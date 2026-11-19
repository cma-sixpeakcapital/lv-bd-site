"""LV Construction website (redesign draft).

The pages in site/ are built by tools/sitegen/build_site.py. This app only serves them.
"""
import json
import os
import re
import time
import urllib.request

from flask import Flask, Response, jsonify, request, send_from_directory

app = Flask(__name__)
SITE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "site")

# route -> file in site/
PAGES = {
    "": "index.html",
    "package": "package.html",
    "how-we-price": "how-we-price.html",
    "rom-to-gmp": "rom-to-gmp.html",
    "projects": "projects.html",
    "affordable-housing": "affordable-housing.html",
    "team": "team.html",
    "contact": "contact.html",
    "subcontractors": "subcontractors.html",
}

# Only these hosts may be listed by search engines. Any other address
# (a preview on onrender.com, a local run) is kept out of search results.
LIVE_HOSTS = {"lvllc.com", "www.lvllc.com"}


def is_live_host():
    return request.host.split(":")[0].lower() in LIVE_HOSTS


@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def page(path):
    key = path.strip("/")
    name = PAGES.get(key)
    if name is None and re.fullmatch(r"projects/[a-z0-9-]+", key):
        # one page per completed building: /projects/<name> is site/projects-<name>.html
        candidate = "projects-" + key.split("/", 1)[1] + ".html"
        if os.path.isfile(os.path.join(SITE_DIR, candidate)):
            name = candidate
    if name is None:
        return send_from_directory(SITE_DIR, "404.html"), 404
    return send_from_directory(SITE_DIR, name)


# ---------------------------------------------------------------- contact form
# The form on /contact posts here. Each note is emailed to the people named in the service's
# environment settings, and a reply goes straight to the person who wrote. Email leaves over
# HTTPS through Resend (resend.com), because Render's free plan blocks the ordinary mail ports.
# Nothing is sent until the settings below are filled in on Render (see the README):
#   RESEND_API_KEY   the sending key
#   CONTACT_TO       who receives each note (Tom)
#   CONTACT_CC       who is copied (Chris); several addresses are separated by commas
#   CONTACT_FROM     the sender shown, on a domain verified with Resend
def _addresses(name):
    return [a.strip() for a in os.environ.get(name, "").split(",") if a.strip()]


CONTACT_TO = _addresses("CONTACT_TO")
CONTACT_CC = _addresses("CONTACT_CC")
CONTACT_FROM = os.environ.get("CONTACT_FROM", "LV Construction website <website@lvllc.com>")
RESEND_API_KEY = os.environ.get("RESEND_API_KEY", "")

FIELDS = [  # (form name, label in the email, longest accepted)
    ("name", "Name", 200), ("company", "Company", 200), ("email", "Email", 200), ("phone", "Phone", 60),
    ("address", "Project address", 300), ("units", "Approximate units", 60), ("stage", "Where it stands", 80),
    ("link", "Plan set link", 600), ("message", "Note", 4000),
]
EMAIL_RE = re.compile(r"^[^@\s<>,;]+@[^@\s<>,;]+\.[^@\s<>,;]+$")
_recent = {}  # address -> times of recent notes, so one sender cannot flood the inbox


def _too_many(ip, limit=5, window=3600):
    now = time.time()
    hits = [t for t in _recent.get(ip, []) if now - t < window]
    if len(_recent) > 5000:
        _recent.clear()
    if len(hits) >= limit:
        _recent[ip] = hits
        return True
    _recent[ip] = hits + [now]
    return False


def _send_email(subject, text, reply_to):
    payload = {"from": CONTACT_FROM, "to": CONTACT_TO, "reply_to": reply_to, "subject": subject, "text": text}
    if CONTACT_CC:
        payload["cc"] = CONTACT_CC
    req = urllib.request.Request(
        "https://api.resend.com/emails", data=json.dumps(payload).encode("utf-8"), method="POST",
        headers={"Authorization": "Bearer " + RESEND_API_KEY, "Content-Type": "application/json", "User-Agent": "contact-form/1.0"},
    )
    with urllib.request.urlopen(req, timeout=12) as resp:
        return 200 <= resp.status < 300


@app.route("/api/contact", methods=["POST"])
def contact():
    wants_json = request.is_json
    src = (request.get_json(silent=True) or {}) if wants_json else request.form

    def reply(ok, status=200, error=""):
        if wants_json:
            return jsonify(ok=ok, error=error), status
        # a browser with scripts off posts the form directly
        line = ("Thank you. Your note is with Tom." if ok else
                "This did not send. Please call Tom at (724) 272-0182.")
        return Response(f'<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">'
                        f'<title>LV Construction</title><body style="font-family: system-ui, sans-serif; padding: 48px 24px; color: #0B1833">'
                        f'<p style="font-size: 20px">{line}</p><p><a href="/contact" style="color: #A84A15">Back to the contact page</a></p>', status=status, mimetype="text/html")

    data = {}
    for key, _label, cap in FIELDS:
        value = str(src.get(key) or "").strip()[:cap]
        data[key] = value if key == "message" else " ".join(value.split())      # one line each: nothing can add a header
    if not data["name"] or not EMAIL_RE.match(data["email"]):
        return reply(False, 400, "Please add your name and an email address Tom can reply to.")

    # Automated junk: a filled-in hidden field, or a form sent within two seconds of loading.
    # It gets the same answer as a real note, and nothing is sent.
    try:
        elapsed = int(src.get("elapsed") or 0)
    except (TypeError, ValueError):
        elapsed = 0
    if str(src.get("website") or "").strip() or (wants_json and elapsed < 2000):
        return reply(True)

    ip = (request.headers.get("X-Forwarded-For", request.remote_addr or "").split(",")[0]).strip()
    if _too_many(ip):
        return reply(False, 429, "Too many notes from this connection. Please call Tom.")

    lines = [f"{label}: {data[key]}" for key, label, _cap in FIELDS if key != "message" and data[key]]
    text = ("\n".join(lines) + "\n\n" + (data["message"] or "(no note)")
            + "\n\n-- \nSent from the contact form on " + request.host + ". Reply to answer " + data["name"] + " directly.")
    subject = "Website inquiry: " + data["name"] + (", " + data["company"] if data["company"] else "")
    if not is_live_host():
        subject = "[Draft site test] " + subject

    if not (RESEND_API_KEY and CONTACT_TO):
        app.logger.warning("Contact form: the sending settings are not filled in, so nothing was sent.")
        return reply(False, 503, "The form is not connected yet.")
    try:
        sent = _send_email(subject[:200], text, data["email"])
    except Exception as exc:  # the visitor is told to reach Tom directly; the cause is in the service log
        app.logger.error("Contact form: sending failed: %s", exc)
        sent = False
    return reply(True) if sent else reply(False, 502, "Sending failed.")


@app.route("/robots.txt")
def robots():
    body = "User-agent: *\nAllow: /\n" if is_live_host() else "User-agent: *\nDisallow: /\n"
    return Response(body, mimetype="text/plain")


@app.route("/favicon.ico")
def favicon():
    return send_from_directory(os.path.join(app.static_folder, "site", "img"), "favicon.png", mimetype="image/png")


@app.after_request
def headers(resp):
    if not is_live_host():
        resp.headers["X-Robots-Tag"] = "noindex, nofollow"
    if request.path.startswith("/static/site/"):
        resp.headers["Cache-Control"] = "public, max-age=3600"
    return resp


if __name__ == "__main__":
    app.run(debug=True, port=5002)
