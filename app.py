"""LV Construction website (redesign draft).

The pages in site/ are built by tools/sitegen/build_site.py. This app only serves them.
"""
import os

from flask import Flask, Response, request, send_from_directory

app = Flask(__name__)
SITE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "site")

# route -> file in site/
PAGES = {
    "": "index.html",
    "package": "package.html",
    "how-we-price": "how-we-price.html",
    "rom-to-gmp": "rom-to-gmp.html",
    "projects": "projects.html",
    "projects/reading": "projects-reading.html",
    "affordable-housing": "affordable-housing.html",
    "team": "team.html",
    "contact": "contact.html",
}

# Only these hosts may be listed by search engines. Any other address
# (a preview on onrender.com, a local run) is kept out of search results.
LIVE_HOSTS = {"lvllc.com", "www.lvllc.com"}


def is_live_host():
    return request.host.split(":")[0].lower() in LIVE_HOSTS


@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def page(path):
    name = PAGES.get(path.strip("/"))
    if name is None:
        return send_from_directory(SITE_DIR, "404.html"), 404
    return send_from_directory(SITE_DIR, name)


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
