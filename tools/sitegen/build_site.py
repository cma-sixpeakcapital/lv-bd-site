#!/usr/bin/env python3
"""Build the draft LV Construction site from the approved round 2 mockups.

    python3 tools/sitegen/build_site.py

Writes one HTML file per page into site/ and the stylesheet into static/site/. Needs only the Python standard library.

How the pages are made
- gen.py and gen2.py are the mockup generator Chris reviewed on the design canvas (round 2, "Light editorial").
  Each page function returns the page body at desktop width or at phone width.
- This script calls every page function twice and puts both layouts in one page:
  the desktop layout shows from 900px up (scaled down between 900px and 1199px), the phone layout shows below 900px.
  Only the layout that is showing loads its photos.
- Copy, numbers and photos are edited in gen.py / gen2.py, then this script is run again. Do not edit site/*.html by hand.

Still placeholders in the pages: everything in [square brackets], the map, the explainer video, the one-page PDF,
and the contact form, which does not send anywhere yet.
"""
import os, re, sys, html

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)
import gen, gen2

# page key -> (route, file, browser title, description)
PAGES = {
    'Home': ('/', 'index.html', 'LV Construction | Los Angeles general contractor',
             'LV Construction builds wood-frame apartment and tax credit housing in Los Angeles, and prices your building from what its own buildings cost.'),
    'Package': ('/package', 'package.html', 'The number in your envelope | LV Construction',
                'How the number LV Construction sent you was built, what it is and is not, and how to get the full breakdown.'),
    'HowWePrice': ('/how-we-price', 'how-we-price.html', 'How we price | LV Construction',
                   'LV Construction estimates from subcontracts it has bought out on its own buildings: the bid library, the process and what you receive.'),
    'RomToGmp': ('/rom-to-gmp', 'rom-to-gmp.html', 'ROM to GMP: when a construction number becomes a guarantee | LV Construction',
                 'A ROM is a budget. A GMP is a guarantee. The guarantee takes hard bids and a verified start date.'),
    'Projects': ('/projects', 'projects.html', 'Projects | LV Construction',
                 'Wood-frame apartment buildings in the City of Los Angeles: completed, under construction and awarded.'),
    'Project_Reading': ('/projects/reading', 'projects-reading.html', 'Reading, Westchester | LV Construction',
                        '8833 Reading Ave, Westchester: developed by Six Peak Capital and built by LV Construction.'),
    'Affordable': ('/affordable-housing', 'affordable-housing.html', 'Affordable housing | LV Construction',
                   'LV Affordable Construction LP builds 4% tax credit housing in Los Angeles, bonded, for sponsors, lenders and investors.'),
    'Team': ('/team', 'team.html', 'Team | LV Construction', 'The people who would build your job: LV Construction leadership, project management, superintendents and office.'),
    'TalkToTom': ('/contact', 'contact.html', 'Contact us | LV Construction', 'Tell Tom Taggart what you are building and where it stands.'),
}

# mockup image key -> file under static/site/img/
IMG = '/static/site/img/'
ASSETS = {'berry': 'berryman-1-dusk.jpg', 'berry2': 'berryman-2.jpg', 'reading': 'reading.jpg', 'wilton': 'wilton.jpg', 'venice': 'venice.jpg',
          'oxford2': 'oxford.jpg', 'reading3': 'reading-corner.jpg', 'reading5': 'reading-street.jpg', 'reading10': 'reading-roof-deck.jpg',
          'reading8': 'reading-interior.jpg', 'grady': 'team/grady-lakamp.jpg', 'logo': 'lv-construction-logo.png'}
for k in list(gen.BLOB):
    gen.BLOB[k] = IMG + (ASSETS[k] if k in ASSETS else 'team/' + k[len('team_'):] + '.jpg')

gen2.target = lambda key, m: PAGES[key][0]     # links go to real routes instead of canvas artboards

TOM = re.compile(r'<div style="width: (\d+)px; height: \d+px; flex: none;[^"]*">\[Photo: Tom Taggart\]</div>')
FORM_NOTE = ('<p style="grid-column: 1 / -1; margin: 0; font-size: 14px; color: #475569">Draft site: this form is not connected yet and sends nothing.</p>')


def body(fn, m):
    b = TOM.sub(lambda mo: f'<img src="{gen.BLOB["team_tom-taggart"]}" alt="Tom Taggart" style="width: {mo.group(1)}px; height: {mo.group(1)}px; '
                           f'flex: none; object-fit: cover; display: block">', fn(m))
    assert '[Photo: Tom Taggart]' not in b
    b = gen2.wire(b, m)
    # photos load only when their layout is showing; the logo loads at once
    b = re.sub(r'<img (?![^>]*alt="LV Construction")', '<img loading="lazy" decoding="async" ', b)
    b = b.replace('<form style=', '<form onsubmit="return false" style=').replace('</form>', FORM_NOTE + '</form>')
    if m:   # the phone layout is a second copy of the page: keep element ids unique
        b = re.sub(r'\b(id|for|aria-labelledby|aria-describedby|aria-controls)="([^"]+)"', lambda mo: f'{mo.group(1)}="m-{mo.group(2)}"', b)
    assert '/_blob/' not in b and '.dc.html' not in b
    return b


t = gen2.t
SHELL = '''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="icon" type="image/png" href="/static/site/img/favicon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&amp;family=DM+Sans:wght@500;600;700&amp;display=swap">
<link rel="stylesheet" href="/static/site/site.css">
</head>
<body>
<div class="lv vd">{desktop}</div>
<div class="lv vm">{phone}</div>
</body>
</html>
'''

CSS = f'''/* Written by tools/sitegen/build_site.py. Do not edit by hand. */
html {{ -webkit-text-size-adjust: 100%; text-size-adjust: 100%; }}
body {{ margin: 0; background: {t["bg"]}; }}
.lv {{ width: 100%; box-sizing: border-box; background: {t["bg"]}; color: {t["text"]}; font-family: {gen.FONT}; font-size: 17px; line-height: 1.5; overflow-x: clip; }}
.lv a {{ color: {t["link"]}; }}
.lv a:hover {{ color: {t["linkh"]}; }}
.lv img {{ max-width: 100%; }}
.lv h1, .lv h2 {{ text-wrap: balance; }}
.lv :focus-visible {{ outline: 3px solid #E8935A; outline-offset: 2px; }}
{gen2.NAV_CSS}
/* Two layouts per page: desktop from 900px, phone below. */
.vm {{ display: none; }}
@media (max-width: 899.98px) {{ .vd {{ display: none; }} .vm {{ display: block; }} }}
/* The desktop layout is drawn for 1200px and wider; between 900px and 1199px it is scaled to fit. */
@media (min-width: 900px) and (max-width: 959.98px) {{ .vd {{ zoom: 0.75; }} }}
@media (min-width: 960px) and (max-width: 1019.98px) {{ .vd {{ zoom: 0.80; }} }}
@media (min-width: 1020px) and (max-width: 1079.98px) {{ .vd {{ zoom: 0.85; }} }}
@media (min-width: 1080px) and (max-width: 1139.98px) {{ .vd {{ zoom: 0.90; }} }}
@media (min-width: 1140px) and (max-width: 1199.98px) {{ .vd {{ zoom: 0.95; }} }}
/* On tablets the phone layout is wide: keep headshots from filling the screen. */
@media (min-width: 560px) and (max-width: 899.98px) {{ .vm img[style*="aspect-ratio: 1 / 1"] {{ max-width: 340px; }} }}
@media (prefers-reduced-motion: reduce) {{ .lv * {{ transition: none !important; }} }}
'''


def main():
    os.makedirs(os.path.join(ROOT, 'site'), exist_ok=True)
    os.makedirs(os.path.join(ROOT, 'static', 'site'), exist_ok=True)
    used, dead = set(), {}
    for key, name, fn in gen2.PAGES:
        route, fname, title, desc = PAGES[key]
        d, p = body(fn, False), body(fn, True)
        page = SHELL.format(title=html.escape(title), desc=html.escape(desc, quote=True), desktop=d, phone=p)
        assert '—' not in page, key
        open(os.path.join(ROOT, 'site', fname), 'w', encoding='utf-8').write(page)
        used |= set(re.findall(r'/static/site/img/([^"\')]+)', page))
        dead[fname] = sorted(set(re.findall(r'<a href="#"[^>]*>(?:<svg.*?</svg>)?([^<]{0,60})', d)))
        print(f'{route:22s} site/{fname:24s} {len(page) // 1024:4d} KB')
    open(os.path.join(ROOT, 'static', 'site', 'site.css'), 'w', encoding='utf-8').write(CSS)
    nf = lambda m: (gen2.nav(m, None) + gen2.sec(t, m, gen2.head(m, 'Page not found', 'That page is not here.', 'It may have moved when the site was rebuilt.')
                    + '<div style="height: 28px"></div>' + gen2.btn(t, m, 'Projects') + '&nbsp; ' + gen2.btn(t, m, 'Contact us', primary=False)) + gen.footer(t, m))
    open(os.path.join(ROOT, 'site', '404.html'), 'w', encoding='utf-8').write(
        SHELL.format(title='Page not found | LV Construction', desc='Page not found.', desktop=body(nf, False), phone=body(nf, True)))
    missing = sorted(u for u in used if not os.path.exists(os.path.join(ROOT, 'static', 'site', 'img', u)))
    print('images used:', len(used), '| missing files:', missing or 'none')
    print('links that lead nowhere yet:')
    for f, labels in dead.items():
        if labels:
            print(' ', f, labels)


if __name__ == '__main__':
    main()
