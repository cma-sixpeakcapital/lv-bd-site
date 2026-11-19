#!/usr/bin/env python3
"""Round 2 LV website mockups: direction B (Light editorial) across the launch pages, desktop and phone."""
import json, os, sys, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gen
from gen import px, wrap, sec, eyebrow, h2, lead, btn, textlink, logo, icon, h1, FONT, DISP, RUST

OUT = '/home/claude/lvmock/root2/project'
gen.BLOB.clear()
gen.BLOB.update({
    'berry': '/_blob/3587ad29778b12db99baf75607e4ef53', 'berry2': '/_blob/7576e6dda3c712626a14073fbfa5db8c',
    'reading': '/_blob/b520a826c4bb199665315c94d08c47a9', 'wilton': '/_blob/35f915d885e2e0809d8337d987cd8bf0',
    'venice': '/_blob/4accb5d2aa372b0b90edb6a8ea48ffb0', 'logo': '/_blob/aa3ce238d742aea51b453a4822e3ef15',
    'reading3': '/_blob/90638a3209ad3c97a5b4d4571bfa6b32', 'reading5': '/_blob/708ce7fc0583fb515a56bdf56fa37887',
    'reading10': '/_blob/cd1f2945bffc085750e142377b4a5d61', 'reading8': '/_blob/a7f658a6b00192e6c37138d03defd8c2',
    'oxford2': '/_blob/d1e37e562e1a20cd7df172b714d599ee', 'grady': '/_blob/9c5e67357f3d17bbf70fc1cfda21763d',
})
gen.BLOB.update({'team_' + k: '/_blob/' + v for k, v in {'alex-rodriguez': 'ffa4fed37251204414f3b5500b84b49a', 'alfredo-tapia': '385a7dfa66d67751310c9be734d51ec1', 'alina-akopians': '35fd30a44459362e8795bf020a8e99aa', 'bob-kennedy': '7c98a65509698b06ad69f9a76c347835', 'brisa-sanchez': '06f5edadfdd7ea9c93d79ecfd24ad039', 'carlos-rocha': '644f44136f61edc6b578b76793a031bf', 'chris-aiello': '25a82112e6eb9fc70782976175e3f6f2', 'chris-andresen': 'cb780622c54af8559cd314fee6a5006f', 'daniel-carillo': 'fe3c39afeaf76f7e8f6db1bd869137dc', 'derek-sanders': 'd47a266da34a48f26dbc461f894944d6', 'devis-tejada': 'fde35379f41e8d2c8c42511ebc3da907', 'dorian-puentes': 'd8933eea1712fbd9cd59d508912ebc1d', 'grady-lakamp': '7a089a16febd800cceed99318683ea25', 'greg-smith': '07d6cf43b0999b1686e41f65ba60a4ae', 'ivan-delgado': '60b04d16fbfdcf4f37f352b0b777edd2', 'jesus-castellanos': '4593b663e6707e43d1730b85f3c7ed8c', 'joe-lakamp': '9ea88044b8207069bda2e0a57abc214a', 'jonah-dobkin': 'f9380224eec0ebecb42886eccb347616', 'justin-krueger': '9a4013009f4a41033e12264806e04770', 'kim-moreno': 'c147351bb22131d600fb7fba553bad0c', 'logan-terriquez': '43e2a088d6be608f7c2dc20a2027bcc1', 'mike-savaikie': 'd37b090db56c5b10b39af3c0a9c65550', 'nick-donald': 'eafab29775354a98324ce663916fe084', 'pedro-rosales': 'ce0ecaaa32ff5b8f46ca0f28c935dad9', 'priscilla-hernandez': '72a9e81f64b9cca4971da5b71091a2e4', 'robert-carrega': '92e02a7da8eb86c144bc9f398be4a26d', 'roy-torres': '6daeebf9bddfde07048e5146d58b86e9', 'sammy-lozano': '7e8edf3b29feead16c59ed9c8f5f53ee', 'steven-garcia': 'da39f9cd3931483b099b53e77b5596b7', 'taylor-flores': 'fda5af262732ae2fd961ffafaa75461c', 'tom-taggart': '27fa1b8482a2fb7e1341b14c8ce0875e'}.items()})
B = gen.BLOB
t = gen.T['B']
TX, MU, BD, EB = t['text'], t['muted'], t['border'], t['eyebrow']
NAV = [('How we price', 'price', 'HowWePrice'), ('ROM to GMP', 'gmp', 'RomToGmp'), ('Projects', 'projects', 'Projects'),
       ('Affordable housing', 'afford', 'Affordable'), ('Team', 'team', 'Team')]
NAV_STYLE = 'B'          # the banner used on every page; A, B and C are drawn side by side on the Banner options board
DENIM, SPACE, GHOST, GLOW = '#0B1833', '#1E2C44', '#F8F9F4', '#E8935A'
NAV_CSS = (
    '.nvA,.nvB,.nvC,.nvBtn{transition:background-color .15s ease,color .15s ease,box-shadow .15s ease}\n'
    '.nvA:hover{background:#0B1833!important;color:#FFFFFF!important;border-color:#0B1833!important}\n'
    '.nvB:hover{background:#1E2C44!important;color:#FFFFFF!important;box-shadow:inset 0 -4px 0 #C4581A}\n'
    '.nvC:hover{color:#FFFFFF!important;box-shadow:inset 0 -3px 0 #E8935A}\n'
    '.nvBtn:hover{background:#A84A15!important;color:#FFFFFF!important}\n'
    '.nvA:focus-visible,.nvB:focus-visible,.nvC:focus-visible,.nvBtn:focus-visible{outline:3px solid #E8935A;outline-offset:2px}\n')
ARW = ('<svg aria-hidden="true" width="{s}" height="{s}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" '
       'stroke-linejoin="round" style="flex: none"><path d="M5 12h14M13 6l6 6-6 6"></path></svg>')

def target(key, m):
    if key == 'Home':
        return 'Home_Phone.dc.html' if m else 'Main.dc.html'
    return f'{key}_{"Phone" if m else "Desktop"}.dc.html'

def contact_btn(m, big=False):
    h = 48 if (big and not m) else 44
    return (f'<a class="nvBtn" href="{target("TalkToTom", m)}" style="display: inline-flex; align-items: center; justify-content: center; gap: 10px; min-height: {h}px; '
            f'padding: 0 {px(m, 22, 16)}px; background: {RUST}; color: #FFFFFF; font-weight: 700; font-size: {px(m, 17, 16)}px; border-radius: {t["rb"]}px; '
            f'text-decoration: none; white-space: nowrap; flex: none">Contact us{ARW.format(s=16)}</a>')

def nav(m, active=None, minimal=False, style=None):
    """The banner. Same six items on every page: logo (home), five page links, Contact us (Tom's contact page).
    A: button links on a white bar. B: logo row over a full-width Denim tab band. C: one Denim bar."""
    st = style or NAV_STYLE
    cur = lambda key: ' aria-current="page"' if key == active else ''
    home = target('Home', m)
    if st == 'A':
        lg = f'<a href="{home}" aria-label="LV Construction, home" style="display: inline-flex; flex: none">{logo(t, m)}</a>'
        links = ''
        for label, key, tg in NAV:
            on = key == active
            links += (f'<a class="nvA" href="{target(tg, m)}"{cur(key)} style="display: inline-flex; align-items: center; justify-content: center; min-height: 44px; '
                      f'padding: 0 {px(m, 16, 12)}px; font-size: {px(m, 16, 15)}px; font-weight: 600; text-decoration: none; white-space: nowrap; box-sizing: border-box; '
                      f'border: 1px solid {DENIM if on else "rgba(11,24,51,0.14)"}; border-radius: {t["rb"]}px; '
                      f'background: {DENIM if on else "#F1F3F7"}; color: {"#FFFFFF" if on else DENIM}">{label}</a>')
        if m:
            inner = (f'<div style="display: flex; align-items: center; justify-content: space-between; gap: 12px; min-height: 72px">{lg}{contact_btn(m)}</div>'
                     f'<nav aria-label="Main" style="display: flex; flex-wrap: wrap; gap: 8px; padding: 0 0 14px">{links}</nav>')
        else:
            inner = (f'<div style="display: flex; align-items: center; justify-content: space-between; gap: 16px; min-height: 92px">{lg}'
                     f'<nav aria-label="Main" style="display: flex; gap: 8px">{links}</nav>{contact_btn(m, True)}</div>')
        return f'<header style="background: #FFFFFF; border-bottom: 1px solid {BD}">{wrap(m, inner)}</header>'
    if st == 'B':
        lg = f'<a href="{home}" aria-label="LV Construction, home" style="display: inline-flex; flex: none">{logo(t, m, h=px(m, 52, 38))}</a>'
        top = f'<div style="display: flex; align-items: center; justify-content: space-between; gap: 16px; min-height: {px(m, 92, 72)}px">{lg}{contact_btn(m, True)}</div>'
        tabs = ''
        n = len(NAV)
        for i, (label, key, tg) in enumerate(NAV):
            on = key == active
            span = (f'grid-column: span {2 if i < 3 else 3}; ' if m else 'flex: 1 1 auto; ')
            edge = 'border-right: 1px solid rgba(255,255,255,0.16); ' if (not m and i == n - 1) else ''
            sep = ('border-left: 1px solid rgba(255,255,255,0.16); ' if not m else
                   ('border-left: 1px solid rgba(255,255,255,0.16); ' if i not in (0, 3) else '') + ('border-top: 1px solid rgba(255,255,255,0.16); ' if i >= 3 else ''))
            tabs += (f'<a class="nvB" href="{target(tg, m)}"{cur(key)} style="{span}display: flex; align-items: center; justify-content: {px(m, "space-between", "center")}; gap: 10px; '
                     f'min-height: {px(m, 60, 48)}px; padding: 0 {px(m, 20, 6)}px; font-size: {px(m, 17, 15)}px; font-weight: 600; text-decoration: none; white-space: nowrap; '
                     f'box-sizing: border-box; {sep}{edge}color: #FFFFFF; background: {SPACE if on else "transparent"}; '
                     f'{"box-shadow: inset 0 -4px 0 " + RUST + "; " if on else ""}">'
                     f'<span>{label}</span>{"" if m else "<span style=\"display: inline-flex; color: " + GLOW + "\">" + ARW.format(s=17) + "</span>"}</a>')
        band = (f'<nav aria-label="Main" style="display: grid; grid-template-columns: repeat(6, minmax(0, 1fr))">{tabs}</nav>' if m else
                wrap(m, f'<nav aria-label="Main" style="display: flex">{tabs}</nav>'))
        return f'<header style="background: #FFFFFF">{wrap(m, top)}<div style="background: {DENIM}">{band}</div></header>'
    # C: one Denim bar
    lg = (f'<a href="{home}" aria-label="LV Construction, home" style="display: inline-flex; flex: none; background: {GHOST}; padding: {px(m, "9px 14px", "7px 11px")}; '
          f'border-radius: {t["rb"]}px">{logo(t, m, h=px(m, 42, 32))}</a>')
    links = ''
    for label, key, tg in NAV:
        on = key == active
        links += (f'<a class="nvC" href="{target(tg, m)}"{cur(key)} style="display: inline-flex; align-items: center; min-height: {px(m, 92, 44)}px; padding: 0 {px(m, 4, 0)}px; '
                  f'font-size: {px(m, 16, 15)}px; font-weight: 600; text-decoration: none; white-space: nowrap; box-sizing: border-box; '
                  f'color: {"#FFFFFF" if on else "#DCE2EC"}; {"box-shadow: inset 0 -3px 0 " + GLOW + "; " if on else ""}">{label}</a>')
    if m:
        inner = (f'<div style="display: flex; align-items: center; justify-content: space-between; gap: 12px; min-height: 76px">{lg}{contact_btn(m)}</div>'
                 f'<nav aria-label="Main" style="display: flex; flex-wrap: wrap; gap: 0 20px; border-top: 1px solid rgba(255,255,255,0.16); padding: 2px 0 6px">{links}</nav>')
    else:
        inner = (f'<div style="display: flex; align-items: center; justify-content: space-between; gap: 16px; min-height: 92px">{lg}'
                 f'<nav aria-label="Main" style="display: flex; gap: 30px">{links}</nav>{contact_btn(m, True)}</div>')
    return f'<header style="background: {DENIM}">{wrap(m, inner)}</header>'

WIRE = {'How we price': 'HowWePrice', 'ROM to GMP': 'RomToGmp', 'Projects': 'Projects', 'All projects': 'Projects', 'Affordable housing': 'Affordable', 'Team': 'Team',
        'Talk to Tom': 'TalkToTom', 'Contact us': 'TalkToTom', 'Book a call': 'TalkToTom', 'Send a plan set': 'TalkToTom', 'Get the full breakdown': 'TalkToTom',
        'Ask for the cost sheet': 'TalkToTom', 'Received a package from us?': 'Package', 'Watch the 90-second explainer': 'RomToGmp',
        'See when the number becomes a guarantee': 'RomToGmp'}

def wire(body, m):
    """Point every button and text link at the artboard it leads to, so the canvas can be clicked through."""
    for label, tg in WIRE.items():
        body = re.sub(r'<a href="#"([^>]*)>((?:<svg.*?</svg>)?)' + re.escape(label) + r'</a>',
                      lambda mo: f'<a href="{target(tg, m)}"{mo.group(1)}>{mo.group(2)}{label}</a>', body)
    body = re.sub(r'<a href="#"( style="display: block; text-decoration: none;[^>]*>)(<img[^>]*alt="Reading,)', lambda mo: f'<a href="{target("Project_Reading", m)}"{mo.group(1)}{mo.group(2)}', body)
    return body

def head(m, eb, title, sub=None, mw=820):
    s = f'{eyebrow(t, eb)}<div style="height: 14px"></div>{h2(t, m, title, mw)}'
    if sub:
        s += f'<div style="height: 16px"></div>{lead(t, m, sub)}'
    return s

def grid(m, n, inner, gap=32, mgap=24):
    return f'<div style="display: grid; grid-template-columns: repeat({px(m,n,1)}, minmax(0, 1fr)); gap: {px(m,gap,mgap)}px">{inner}</div>'

def ruled(m, title, text, strong=True, num=None):
    n = f'<div style="font-size: 13px; font-weight: 700; letter-spacing: 0.2em; color: {EB}">{num}</div>' if num else ''
    return (f'<div style="border-top: {2 if strong else 1}px solid {TX}; padding-top: 18px; display: flex; flex-direction: column; gap: 10px">{n}'
            f'<h3 style="margin: 0; font-family: {DISP}; font-weight: 600; font-size: {px(m,24,21)}px; line-height: 1.2; color: {TX}">{title}</h3>'
            f'<p style="margin: 0; font-size: 16px; line-height: 1.55; color: {MU}">{text}</p></div>')

def page_hero(m, eb, title, sub, cta=None, d=68, mw=980, pb=None):
    c = f'<div style="height: 32px"></div>{cta}' if cta else ''
    inner = (f'{eyebrow(t, eb)}<div style="height: 22px"></div>{h1(t, m, title, d=d, p=38, mw=mw)}<div style="height: {px(m,26,20)}px"></div>'
             f'{lead(t, m, sub, 700)}{c}')
    return sec(t, m, inner, pt=px(m, 88, 44), pb=(px(m, 72, 40) if pb is None else pb))

def stat_row(m, items):
    cells = ''
    for i, (n, l) in enumerate(items):
        bl = '' if (i == 0 or (m and i % 2 == 0)) else f'border-left: 1px solid {BD}; padding-left: {px(m,32,18)}px; '
        cells += (f'<div style="{bl}"><div style="font-family: {DISP}; font-weight: 600; font-size: {px(m,52,36)}px; line-height: 1; letter-spacing: -0.02em; color: {RUST if i == 0 else TX}">{n}</div>'
                  f'<div style="margin-top: 12px; font-size: 15px; line-height: 1.4; color: {MU}">{l}</div></div>')
    return (f'<div style="border-top: 2px solid {TX}; padding-top: {px(m,32,24)}px; display: grid; grid-template-columns: repeat({px(m,len(items),2)}, minmax(0, 1fr)); gap: {px(m,32,24)}px">{cells}</div>')

def placeholder(text, ratio='16 / 9', dark=False):
    bg, col = ('#0B1833', '#BFC7DA') if dark else ('#E2E7F0', '#475569')
    return (f'<div style="aspect-ratio: {ratio}; background: {bg}; display: flex; flex-direction: column; gap: 14px; align-items: center; justify-content: center; text-align: center; padding: 20px; box-sizing: border-box; '
            f'font-size: 15px; color: {col}">{icon(gen.IC_PLAY, col, 56) if dark else ""}<span>{text}</span></div>')

# =================================================================== HOW WE PRICE
BEHIND = [('Committed costs, not quotes', 'Rates come from executed subcontracts and audited final costs, reconciled from GMP through change orders to final payment. Quotes run lower than buyout; we price where trades actually land.'),
          ('Your drawings drive it', 'Quantities, construction type, parking, HVAC system, finishes and cladding are read off the plan set and cited by sheet. Where the plans are silent, the assumption is stated, never buried.'),
          ('Current market, dated', 'The library is weighted toward recent buyouts and refreshed against live job costs, so each estimate carries a market as-of date and reflects today\'s trade pricing.')]
RECEIVE = [('A full line-item budget', 'In our GMP format, each line with cost per square foot and per unit.'),
           ('A scope-confidence flag on every line', 'Tight, Moderate or Wide, from real bid spreads, so you see where scope needs tightening.'),
           ('A plan-cited clarifications list', 'Each input marked Confirmed with its sheet, or Assumed with the reason.'),
           ('Value-engineering options', 'Quantified, and drawn from savings we have accepted on past jobs.')]
CANNOT = ['No site visit, and no input from the owner or the design team.',
          'No soils, structural, civil or building systems engineering beyond what the filed set shows.',
          'Scope and quantities are our reading of the drawings and may differ from the current design.',
          'It excludes land, design and other soft costs, permits and fees, utility connection charges, off-site work, furniture and equipment, and owner contingency unless listed.',
          'Pricing is as of a stated date and is not held for any period.']

def badge(kind):
    bg, col = {'Tight': ('rgba(78,122,58,0.12)', '#4E7A3A'), 'Moderate': ('rgba(154,106,18,0.12)', '#9A6A12'), 'Wide': ('rgba(196,88,26,0.12)', '#A84A15'),
               'Confirmed': ('rgba(78,122,58,0.12)', '#4E7A3A'), 'Assumed': ('rgba(154,106,18,0.12)', '#9A6A12')}[kind]
    return f'<span style="display: inline-block; background: {bg}; color: {col}; font-size: 13px; font-weight: 700; padding: 4px 10px; border-radius: 4px">{kind}</span>'

def sample_rom(m):
    rows = ''
    for flag in ['Tight', 'Tight', 'Moderate', 'Moderate', 'Wide']:
        rows += (f'<div style="display: grid; grid-template-columns: minmax(0, 1.4fr) minmax(0, 1fr) minmax(0, 0.8fr) 92px; gap: 12px; align-items: center; padding: 12px 0; border-top: 1px solid {BD}; font-size: 15px; color: {MU}">'
                 f'<span>[Trade division]</span><span style="text-align: right; font-variant-numeric: tabular-nums">[amount]</span><span style="text-align: right">[$ / SF]</span><span>{badge(flag)}</span></div>')
    cl = ''
    for kind, a, b in [('Confirmed', '[Input]', 'Sheet [number]'), ('Assumed', '[Input]', '[Reason]')]:
        cl += (f'<div style="display: grid; grid-template-columns: 104px minmax(0, 1fr) minmax(0, 1fr); gap: 12px; align-items: center; padding: 12px 0; border-top: 1px solid {BD}; font-size: 15px; color: {MU}">'
               f'<span>{badge(kind)}</span><span>{a}</span><span>{b}</span></div>')
    hd = lambda x: f'<div style="font-size: 13px; font-weight: 700; letter-spacing: 0.14em; text-transform: uppercase; color: {TX}; padding-bottom: 10px">{x}</div>'
    return (f'<div style="background: #FFFFFF; border: 1px solid {BD}; padding: {px(m,32,20)}px">'
            f'<div style="display: flex; justify-content: space-between; flex-wrap: wrap; gap: 8px; align-items: baseline; margin-bottom: 18px">'
            f'<div style="font-family: {DISP}; font-weight: 600; font-size: 21px; color: {TX}">Rough order of magnitude estimate</div>'
            f'<div style="font-size: 13px; color: {MU}">Sample layout. Figures removed.</div></div>'
            f'{hd("Budget by trade division")}{rows}<div style="height: 22px"></div>{hd("Clarifications")}{cl}</div>')

def page_price(m):
    cta = f'<div style="display: flex; flex-wrap: wrap; gap: 14px">{btn(t, m, "Send a plan set", full=m)}{btn(t, m, "Received a package from us?", primary=False, full=m)}</div>'
    hero = page_hero(m, 'How we price', 'Priced from what we have actually paid, not from what someone estimated.',
                     'Every LV rough order of magnitude estimate starts with your drawings and prices each line from our own library of bought-out subcontract costs on Los Angeles multifamily projects. '
                     'One defensible number per line, with every assumption traced to a plan sheet.', cta, pb=px(m, 24, 8))
    behind = sec(t, m, head(m, 'Behind the number', 'What stands behind every line') + f'<div style="height: {px(m,40,26)}px"></div>'
                 + grid(m, 3, ''.join(ruled(m, a, b) for a, b in BEHIND)))
    st = gen.steps(t, m, title='Four steps from plan set to number', bg=t['bg2'], eb='The process')
    rec_list = ''.join(f'<li style="padding: 16px 0; border-top: 1px solid {BD}"><span style="display: block; font-family: {DISP}; font-weight: 600; font-size: 20px; color: {TX}">{a}</span>'
                       f'<span style="display: block; margin-top: 4px; font-size: 16px; line-height: 1.5; color: {MU}">{b}</span></li>' for a, b in RECEIVE)
    receive = sec(t, m, head(m, 'What you receive', 'More than one number') + f'<div style="height: {px(m,40,26)}px"></div>'
                  + f'<div style="display: grid; grid-template-columns: {px(m,"minmax(0, 0.9fr) minmax(0, 1.1fr)","minmax(0, 1fr)")}; gap: {px(m,56,28)}px; align-items: start">'
                  + f'<ul style="list-style: none; margin: 0; padding: 0">{rec_list}</ul>{sample_rom(m)}</div>')
    def chk(big, text):
        return (f'<div style="border-top: 2px solid {TX}; padding-top: 20px"><div style="font-family: {DISP}; font-weight: 600; font-size: {px(m,52,38)}px; line-height: 1; letter-spacing: -0.02em; color: {RUST}">{big}</div>'
                f'<p style="margin: 14px 0 0; font-size: 18px; line-height: 1.5; color: {TX}; max-width: 440px">{text}</p></div>')
    checked = sec(t, m, head(m, 'How it is checked', 'Tested against our own signed and bought-out jobs') + f'<div style="height: {px(m,40,26)}px"></div>'
                  + grid(m, 2, chk('To the dollar', 'The library reproduces a signed $43M GMP through our full markup stack.')
                         + chk('Within 4%', 'of projected final trade cost on two current projects more than 90% bought out.'), gap=56), bg=t['bg2'])
    lis = ''.join(f'<li style="padding: 16px 0; border-top: 1px solid {BD}; font-size: {px(m,18,17)}px; line-height: 1.5; color: {TX}">{x}</li>' for x in CANNOT)
    cannot = sec(t, m, head(m, 'Know its limits', 'What a ROM from a filed plan set cannot see',
                            'A ROM is a hard-cost benchmark. It is not a guaranteed maximum price, a lump-sum bid or an offer.')
                 + f'<div style="height: {px(m,32,20)}px"></div><ul style="list-style: none; margin: 0; padding: 0; max-width: 860px">{lis}</ul>'
                 + f'<div style="margin-top: {px(m,28,20)}px">{textlink(t, "See when the number becomes a guarantee")}</div>')
    return ''.join([nav(m, 'price'), hero, gen.counters(t, m), behind, st, receive, checked, cannot, gen.tom(t, m), gen.footer(t, m, True)])

# =================================================================== ROM TO GMP
STG = [('ROM', 'Rough order of magnitude', 'Built from early plans and our own bid history.', 'Use it to underwrite the deal. It is a budget, not a price.', 'No', 'no', '100%'),
       ('Preconstruction updates', '', 'As the drawings develop, we update the estimate from the new plans and the range narrows.', 'Where it helps, we price larger or less certain trades with subcontractors early. It is still a budget.', 'No', 'no', '66%'),
       ('Hard bid', '', 'With a closing and a start date in clear sight, the job goes to subcontractors for hard bids.', 'Real numbers from real trades, good for a limited time.', 'Not yet', 'notyet', '36%'),
       ('GMP', 'Guaranteed maximum price', 'Hard bids in hand and a verified start date: now LV commits.', 'You pay the cost of the work plus our fee, capped at the GMP for the agreed scope.', 'Yes', 'yes', None)]
FAQ = [('What does a ROM cost?', 'Nothing. It is free, and it is not a bid.'),
       ('What do you need from me?', 'The set you have, at whatever stage it is. A link to the drawings is enough.'),
       ('How long is a ROM good for?', 'Each estimate carries a market as-of date. It is not held for any period.'),
       ('What does the GMP cover?', 'The cost of the work plus our fee, capped at the guaranteed maximum for the agreed scope. A change you direct moves the GMP by change order.'),
       ('Do you hard bid?', 'Yes. With a closing and a start date in sight, we bid every trade to the market and open the book to you. Until then, the number is a budget.'),
       ('Will you bid against other general contractors?', 'We can, and we will if you ask. We do not think it is in your best interest: it can lower the number on paper and raise it in the field. We would rather open the book and put the competition among the trades.')]

def stage_rows(m):
    out = ''
    for i, (name, full, a, b, ans, key, wdt) in enumerate(STG):
        bar = (f'<div style="height: 5px; background: {RUST}; width: 100%"></div>' if wdt is None else
               f'<div style="height: 16px; background: {t["band"]}; width: {wdt}"></div>')
        fl = f'<div style="font-size: 15px; color: {MU}; margin-top: 2px">{full}</div>' if full else ''
        txt = (f'<div><div style="font-family: {DISP}; font-weight: 600; font-size: {px(m,30,24)}px; line-height: 1.15; color: {TX}">{name}</div>{fl}'
               f'<p style="margin: 12px 0 0; font-size: {px(m,18,16)}px; line-height: 1.5; color: {TX}; max-width: 560px">{a}</p>'
               f'<p style="margin: 6px 0 0; font-size: {px(m,18,16)}px; line-height: 1.5; color: {MU}; max-width: 560px">{b}</p>'
               f'<div style="margin-top: 18px; max-width: 560px">{bar}</div></div>')
        num = f'<div style="font-family: {DISP}; font-weight: 600; font-size: {px(m,30,22)}px; color: {EB}">0{i+1}</div>'
        answer = (f'<div style="{px(m,"text-align: right","")}"><div style="font-size: 14px; color: {MU}">Guaranteed?</div>'
                  f'<div style="font-family: {DISP}; font-weight: 700; font-size: {px(m,44,30)}px; line-height: 1.1; color: {t[key]}">{ans}</div></div>')
        if m:
            out += (f'<li style="border-top: 2px solid {TX}; padding: 22px 0 26px"><div style="display: flex; justify-content: space-between; align-items: flex-start; gap: 12px; margin-bottom: 8px">{num}{answer}</div>{txt}</li>')
        else:
            out += (f'<li style="border-top: 2px solid {TX}; padding: 32px 0 40px; display: grid; grid-template-columns: 90px minmax(0, 1fr) 220px; gap: 24px; align-items: start">{num}{txt}{answer}</li>')
    return f'<ol style="list-style: none; margin: 0; padding: 0">{out}</ol>'

def window_graphic(m):
    def row(label, pos, note, ok):
        col = '#4E7A3A' if ok else '#A84A15'
        return (f'<div style="padding: 20px 0; border-top: 1px solid {BD}"><div style="font-family: {DISP}; font-weight: 600; font-size: {px(m,21,19)}px; color: {TX}">{label}</div>'
                f'<div style="position: relative; height: 56px; margin-top: 14px">'
                f'<div style="position: absolute; left: 0; top: 14px; width: 60%; height: 28px; background: {t["band"]}; display: flex; align-items: center; padding-left: 12px; box-sizing: border-box; font-size: 13px; font-weight: 600; color: {TX}">Bid window</div>'
                f'<div style="position: absolute; left: {pos}%; top: 0; width: 4px; height: 56px; background: {col}"></div></div>'
                f'<div style="margin-top: 10px; font-size: 16px; font-weight: 600; color: {col}">{note}</div></div>')
    return (f'<div role="img" aria-label="Two timelines: a start date inside the bid window holds the price; a start date after it reopens the price">'
            + row('Start inside the window', 44, 'The trades hold their prices. The guarantee stands.', True)
            + row('Start after the window', 82, 'The trades re-price. The guarantee has to be reset.', False) + '</div>')

def page_gmp(m):
    video = (f'<figure style="margin: {px(m,56,32)}px 0 0">{placeholder("[Explainer video: 88 seconds, plays muted]", "16 / 9", dark=True)}'
             f'<figcaption style="margin-top: 12px; font-size: 14px; color: {MU}">ROM, hard bid and GMP, explained in 90 seconds.</figcaption></figure>')
    hero = sec(t, m, f'{eyebrow(t, "ROM to GMP")}<div style="height: 22px"></div>{h1(t, m, "When does a construction number become a guarantee?", d=68, p=38, mw=980)}'
               f'<div style="height: {px(m,26,20)}px"></div>{lead(t, m, "A project is priced again and again on the way to construction. Only the last number is guaranteed.", 700)}{video}',
               pt=px(m, 88, 44), pb=px(m, 72, 40))
    stg = sec(t, m, head(m, 'Four stages', 'Four stages. One guarantee.') + f'<div style="height: {px(m,40,24)}px"></div>{stage_rows(m)}', bg=t['bg2'])
    start = sec(t, m, f'<div style="display: grid; grid-template-columns: {px(m,"minmax(0, 1fr) minmax(0, 1fr)","minmax(0, 1fr)")}; gap: {px(m,64,28)}px; align-items: start">'
                f'<div>{head(m, "Why the start date matters", "The guarantee is tied to the day you start.", "Subcontractor bids are only good for a limited window, so we take hard bids when the closing and the start date are real. If the start then slips past the window, the trades re-price and the guarantee has to be reset.")}</div>'
                f'{window_graphic(m)}</div>')
    line = sec(t, m, f'<div style="border-top: 2px solid {TX}; border-bottom: 2px solid {TX}; padding: {px(m,56,32)}px 0">'
               f'<div style="font-family: {DISP}; font-weight: 600; font-size: {px(m,46,28)}px; line-height: 1.12; letter-spacing: -0.01em; text-wrap: balance; color: {TX}; max-width: 980px">'
               f'A ROM is a budget. A GMP is a <span style="color: {RUST}">guarantee</span>. The guarantee takes hard bids and a verified start date.</div></div>', pt=0, pb=px(m, 96, 56))
    qa = ''.join(f'<div style="border-top: 1px solid {TX}; padding: {px(m,24,18)}px 0; display: grid; grid-template-columns: {px(m,"minmax(0, 0.8fr) minmax(0, 1.2fr)","minmax(0, 1fr)")}; gap: {px(m,32,8)}px">'
                 f'<h3 style="margin: 0; font-family: {DISP}; font-weight: 600; font-size: {px(m,22,20)}px; color: {TX}">{q}</h3>'
                 f'<p style="margin: 0; font-size: {px(m,18,16)}px; line-height: 1.55; color: {MU}">{a}</p></div>' for q, a in FAQ)
    dl = (f'<div style="margin-top: {px(m,40,28)}px; display: flex; flex-wrap: wrap; gap: 16px; align-items: center; justify-content: space-between; background: #FFFFFF; border: 1px solid {BD}; padding: {px(m,28,20)}px">'
          f'<div><div style="font-family: {DISP}; font-weight: 600; font-size: 21px; color: {TX}">Explaining this to your lender or equity partner?</div>'
          f'<div style="font-size: 16px; color: {MU}; margin-top: 4px">[One-page PDF: ROM to GMP]</div></div>{btn(t, m, "Download the one-pager", primary=False, full=m)}</div>')
    faq = sec(t, m, head(m, 'Questions', 'What developers ask us') + f'<div style="height: {px(m,32,20)}px"></div>{qa}{dl}', bg=t['bg2'])
    return ''.join([nav(m, 'gmp'), hero, stg, start, line, faq, gen.tom(t, m), gen.footer(t, m, True)])

# =================================================================== PROJECTS
DONE = [('Berryman I', 'Mar Vista', '156', '82,700', '2025', 'berry', 'Berryman I at dusk, seen from above'),
        ('Berryman II', 'Mar Vista', '126', '60,500', '2025', 'berry2', 'Berryman II at dusk, from the street'),
        ('Reading', 'Westchester', '124', '56,200', '2025', 'reading', 'Reading, a five-story blue and white building'),
        ('Wilton', 'Los Angeles', '132', '62,500', '2026', 'wilton', 'Wilton, seen from the street corner'),
        ('Venice', 'Mar Vista', '112', '54,500', '2023', 'venice', 'Venice, a four-story white and black building'),
        ('Oxford', 'Los Angeles', '141', '66,500', '2022', 'oxford2', 'Oxford, a seven-story building seen from above')]
UC = [('2859 Francis Ave', 'Koreatown', '4% tax credit', '232', 'Mar 2029'), ('9033 Ramsgate Ave', 'Westchester', 'Market rate', '116', 'Sep 2027'),
      ('11143 Acama St', 'Studio City', '4% tax credit', '131', '[date]'), ('5365 Crenshaw Blvd', 'South Los Angeles', 'Market rate', '48', 'Dec 2026'),
      ('10953 Whipple St', 'North Hollywood', '4% tax credit', '91', 'Q4 2027'), ('5150 Riverton / 5151 Denny', 'North Hollywood', '4% tax credit', '80', 'Feb 2028'),
      ('11218 Califa St', 'North Hollywood', '4% tax credit', '76', 'Q4 2027'), ('5655 Lexington Ave', 'Hollywood', '4% tax credit', '67', 'Feb 2028'),
      ('5614 Troost Ave', 'Valley Village', 'Market rate', '75', '[date]'),
      ('1172 Nelrose Ave', 'Venice', 'Market rate', '11', 'May 2027')]

def done_card(m, p, ratio='3 / 2'):
    name, hood, u, sf, yr, key, alt = p
    return (f'<a href="#" style="display: block; text-decoration: none; color: {TX}"><img src="{B[key]}" alt="{alt}" style="display: block; width: 100%; aspect-ratio: {ratio}; object-fit: cover">'
            f'<div style="margin-top: 14px; font-family: {DISP}; font-weight: 600; font-size: 24px; color: {TX}">{name}</div>'
            f'<div style="margin-top: 2px; font-size: 15px; color: {MU}">{hood} | Delivered {yr}</div>'
            f'<div style="margin-top: 2px; font-size: 15px; color: {MU}">{u} leasable units | {sf} square feet</div></a>')

def table(m, cols, rows, total=None, widths=None):
    """cols: list of (label, align). Desktop: grid rows. Phone: stacked label/value blocks."""
    if m:
        out = ''
        for r in rows:
            sub = ''.join(f'<div style="display: flex; justify-content: space-between; gap: 12px; font-size: 15px; padding: 2px 0"><span style="color: {MU}">{cols[i][0]}</span><span style="color: {TX}; text-align: right">{r[i]}</span></div>'
                          for i in range(1, len(cols)))
            out += f'<div style="border-top: 1px solid {BD}; padding: 14px 0"><div style="font-family: {DISP}; font-weight: 600; font-size: 19px; color: {TX}; margin-bottom: 6px">{r[0]}</div>{sub}</div>'
        if total:
            out += f'<div style="border-top: 2px solid {TX}; padding: 14px 0; display: flex; justify-content: space-between; font-weight: 700; font-size: 17px; color: {TX}"><span>{total[0]}</span><span>{total[1]}</span></div>'
        return f'<div>{out}</div>'
    gt = widths or ' '.join(['minmax(0, 1.6fr)'] + ['minmax(0, 1fr)'] * (len(cols) - 1))
    hd = ''.join(f'<div style="text-align: {a}">{l}</div>' for l, a in cols)
    out = f'<div style="display: grid; grid-template-columns: {gt}; gap: 24px; padding: 0 0 12px; font-size: 13px; font-weight: 700; letter-spacing: 0.12em; text-transform: uppercase; color: {MU}">{hd}</div>'
    for r in rows:
        cells = ''.join(f'<div style="text-align: {cols[i][1]}; font-variant-numeric: tabular-nums; {"font-family: " + DISP + "; font-weight: 600; font-size: 19px; color: " + TX if i == 0 else "color: " + MU}">{r[i]}</div>' for i in range(len(cols)))
        out += f'<div style="display: grid; grid-template-columns: {gt}; gap: 24px; align-items: baseline; padding: 16px 0; border-top: 1px solid {BD}; font-size: 16px">{cells}</div>'
    if total:
        cells = ''.join(f'<div style="text-align: {cols[i][1]}; font-variant-numeric: tabular-nums">{total[2].get(i, "")}</div>' for i in range(len(cols)))
        out += f'<div style="display: grid; grid-template-columns: {gt}; gap: 24px; padding: 16px 0; border-top: 2px solid {TX}; font-size: 17px; font-weight: 700; color: {TX}">{cells}</div>'
    return f'<div>{out}</div>'

def tabs(m, items):
    chips = ''
    for i, c in enumerate(items):
        on = i == 0
        chips += (f'<button type="button" aria-pressed="{"true" if on else "false"}" style="background: transparent; border: none; border-bottom: 3px solid {RUST if on else "transparent"}; padding: 0 2px; min-height: 48px; '
                  f'font-family: {FONT}; font-size: 17px; font-weight: {700 if on else 500}; color: {TX if on else MU}; border-radius: 0">{c}</button>')
    return f'<div style="border-bottom: 1px solid {BD}; display: flex; flex-wrap: wrap; gap: {px(m,"8px 28px","0 22px")}">{chips}</div>'

# =================================================================== ADDED 19 NOV: partnership, what we build, awarded work, Six Peak
SIXPEAK = 'https://www.sixpeakcapital.com/'

def ext(label, url=SIXPEAK):
    return f'<a href="{url}" style="color: {t["link"]}; font-weight: 600; text-decoration: underline; text-underline-offset: 4px">{label}</a>'

PARTNER = [('One team from the first budget', 'Preconstruction, estimating, project management and field supervision are in-house. The team that budgets your building is the team that builds it.'),
           ('Competition among the trades', 'Every trade is bid to the market, and you see the bids. That is where competition lowers cost without adding risk.'),
           ('Capital when the deal needs it', 'With ' + ext('Six Peak Capital') + ', we advise on capitalization and, in select circumstances, provide credit enhancement and capital for projects.')]

def partnership(m, bg=None):
    body = (head(m, 'How we work', 'Partnership, not competition.',
                 'We would rather be your builder from the first budget than one of several bids at the end. Bidding general contractors against each other can lower the number on paper and raise it in the field, through change orders and delay.')
            + f'<p style="margin: 14px 0 0; max-width: 760px; font-size: {px(m,19,17)}px; line-height: 1.6; color: {TX}; font-weight: 600">We can bid your job against other general contractors, and we will if you ask. We do not think it is in your best interest.</p>'
            + f'<div style="height: {px(m,44,28)}px"></div>' + grid(m, 3, ''.join(ruled(m, a, b) for a, b in PARTNER), gap=40, mgap=24))
    return sec(t, m, body, bg=bg)

BUILD = [('Multifamily', 'Wood-frame, podium and mid-rise apartments, from 11 to 232 units.'),
         ('Mixed-use', 'Ground-floor retail with apartments above, including complex podium structures.'),
         ('Commercial', 'Ground-up commercial, drawing on our podium and concrete experience.'),
         ('Affordable and tax credit', 'Tax credit housing through LV Affordable Construction LP, built for CASp compliance and the investor reporting that tax credit deals require.')]

def what_we_build(m, bg=None):
    body = (head(m, 'What we build', 'Multifamily, mixed-use, commercial and affordable.') + f'<div style="height: {px(m,40,26)}px"></div>'
            + grid(m, 4, ''.join(ruled(m, a, b) for a, b in BUILD), gap=32, mgap=24))
    return sec(t, m, body, bg=bg)

# Awarded and in preconstruction. Reseda per Chris, 19 Nov. Klump and Scott are on the live site as pre-construction.
AWARDED = [('8350 Reseda Blvd', 'Northridge', '4% tax credit', '206'), ('6010 Klump Ave', 'North Hollywood', '100% affordable (ED1)', '53'),
           ('2227 W Scott Ave', 'Silver Lake', '100% affordable (ED1)', '38')]

def page_projects(m):
    hero = page_hero(m, 'Projects', 'Wood-frame apartment buildings in the City of Los Angeles.',
                     '15 buildings completed since 2016, ten under construction and three awarded. Type III and V wood frame, with and without podium or subterranean parking, from 11 to 232 units.', pb=px(m, 40, 24))
    mapsec = sec(t, m, tabs(m, ['All', 'Completed', 'Under construction', 'Awarded', 'Market rate', 'Tax credit']) + f'<div style="height: {px(m,32,20)}px"></div>'
                 + f'<div style="aspect-ratio: {px(m,"21 / 8","4 / 3")}; background: #E2E7F0; display: flex; align-items: center; justify-content: center; text-align: center; padding: 20px; box-sizing: border-box; font-size: 15px; color: {MU}">[Map of Los Angeles: one pin for each LV building]</div>',
                 pt=0, pb=px(m, 72, 40))
    done = sec(t, m, head(m, 'Completed', 'Developed by Six Peak, built by LV') + f'<div style="height: {px(m,40,26)}px"></div>'
               + f'<div style="display: grid; grid-template-columns: repeat({px(m,3,1)}, minmax(0, 1fr)); gap: {px(m,"56px 32px","32px")}">' + ''.join(done_card(m, p) for p in DONE) + '</div>'
               + f'<div style="margin-top: {px(m,40,28)}px; font-size: 15px; color: {MU}">[Nine more completed buildings to add, Bonner and Kenmore among them]</div>', bg=t['bg2'])
    uc = sec(t, m, head(m, 'Under construction', 'Ten projects, 927 units') + f'<div style="height: {px(m,40,24)}px"></div>'
             + table(m, [('Project', 'left'), ('Submarket', 'left'), ('Program', 'left'), ('Units', 'right'), ('Completion', 'right')], UC,
                     total=('Ten projects', '927 units', {0: 'Ten projects', 3: '927'})))
    aw = sec(t, m, head(m, 'Awarded, in preconstruction', 'Three projects, 297 units') + f'<div style="height: {px(m,40,24)}px"></div>'
             + table(m, [('Project', 'left'), ('Submarket', 'left'), ('Program', 'left'), ('Units', 'right')], AWARDED,
                     total=('Three projects', '297 units', {0: 'Three projects', 3: '297'})), pt=0)
    return ''.join([nav(m, 'projects'), hero, mapsec, done, uc, aw, gen.tom(t, m, bg=t['bg2']), gen.footer(t, m)])

# =================================================================== PROJECT PAGE (Reading)
def page_project(m):
    crumb = (f'<nav aria-label="Breadcrumb" style="font-size: 15px; color: {MU}"><a href="#" style="display: inline-flex; align-items: center; min-height: 44px; color: {t["link"]}">Projects</a>'
             f'<span style="margin: 0 10px">/</span><span>Reading</span></nav>')
    top = sec(t, m, f'{crumb}<div style="height: {px(m,24,12)}px"></div>{h1(t, m, "Reading", d=84, p=46)}'
              f'<div style="margin-top: 14px; font-size: {px(m,20,17)}px; color: {MU}">8833 Reading Ave, Westchester | Delivered April 2025</div>'
              f'<figure style="margin: {px(m,48,28)}px 0 0"><img src="{B["reading3"]}" alt="Reading from the street corner: five stories, blue tile and white panels" style="display: block; width: 100%; aspect-ratio: {px(m,"16 / 9","4 / 3")}; object-fit: cover">'
              f'<figcaption style="margin-top: 12px; font-size: 14px; color: {MU}">[Photo credit]</figcaption></figure>'
              f'<div style="height: {px(m,56,32)}px"></div>'
              + stat_row(m, [('124', 'leasable units'), ('56,200', 'square feet'), ('5 levels', 'of Type III-A over a subterranean garage'), ('2025', 'delivered in April')]),
              pt=px(m, 40, 20), pb=px(m, 80, 48))
    facts = [('Developer', 'Six Peak Capital'), ('Builder', 'LV Construction'), ('Structure', 'Type III-A wood frame, five levels, over a subterranean garage'),
             ('Program', '[Program]'), ('Architect', '[Architect]')]
    fl = ''.join(f'<div style="display: grid; grid-template-columns: 130px minmax(0, 1fr); gap: 16px; padding: 14px 0; border-top: 1px solid {BD}; font-size: 16px"><span style="color: {MU}">{a}</span><span style="color: {TX}">{b}</span></div>' for a, b in facts)
    story = sec(t, m, f'<div style="display: grid; grid-template-columns: {px(m,"minmax(0, 1.2fr) minmax(0, 0.8fr)","minmax(0, 1fr)")}; gap: {px(m,64,32)}px; align-items: start">'
                f'<div>{head(m, "The job", "What was hard, and what we did about it")}<div style="height: 20px"></div>'
                f'<p style="margin: 0; font-size: {px(m,19,17)}px; line-height: 1.6; color: {TX}">Five levels of Type III-A wood frame over a subterranean garage. Six Peak developed the building and LV built it.</p>'
                f'<p style="margin: 16px 0 0; font-size: {px(m,19,17)}px; line-height: 1.6; color: {MU}">[Two or three sentences from Grady or Pedro: what was hard on this job, and how it was solved.]</p></div>'
                f'<div>{fl}</div></div>', bg=t['bg2'])
    gal = [('reading5', 'The street front', 'Reading street front: blue tile with orange window frames'), ('reading10', 'Roof deck', 'Roof deck with a shade sail, grill and seating'),
           ('reading8', 'Shared kitchen and dining room', 'Shared kitchen with a long dining table')]
    g = ''.join(f'<figure style="margin: 0"><img src="{B[k]}" alt="{alt}" style="display: block; width: 100%; aspect-ratio: 4 / 3; object-fit: cover"><figcaption style="margin-top: 10px; font-size: 15px; color: {MU}">{c}</figcaption></figure>' for k, c, alt in gal)
    gallery = sec(t, m, grid(m, 3, g, gap=28, mgap=24), pb=px(m, 40, 24))
    more = [gen.PROJ[0], gen.PROJ[2], gen.PROJ[3]]
    others = sec(t, m, head(m, 'More buildings', 'Buildings like this one') + f'<div style="height: {px(m,36,24)}px"></div>'
                 + f'<div style="display: grid; grid-template-columns: repeat({px(m,3,1)}, minmax(0, 1fr)); gap: {px(m,28,28)}px">' + ''.join(gen.pcard(t, m, p) for p in more) + '</div>')
    return ''.join([nav(m, 'projects'), top, story, gallery, others, gen.tom(t, m, bg=t['bg2']), gen.footer(t, m)])

# =================================================================== AFFORDABLE
AFF = [('Bonded', 'Payment and performance bonds are in force on five projects. No bond claims, and no failure to complete awarded work.'),
       ('Ready for your lender and investor', 'We answer lender and investor contractor questionnaires at every closing, and we keep the answers current.'),
       ('A clean record', 'Zero general liability and workers\' compensation claims on loss runs from 2020 forward.'),
       ('One product', 'Type III and V wood frame, with and without podium or subterranean parking. The same buildings we build at market rate.')]
LIHTC = [r for r in UC if r[2] == '4% tax credit']

def page_afford(m):
    cta = f'<div style="display: flex; flex-wrap: wrap; gap: 14px">{btn(t, m, "Talk to Tom", full=m)}{btn(t, m, "Send a plan set", primary=False, full=m)}</div>'
    hero = page_hero(m, 'Affordable housing', 'Tax credit housing, built by a team that closes tax credit deals itself.',
                     'LV Affordable Construction LP builds 4% tax credit housing. Its owner group develops and invests in tax credit projects of its own, so we know what the lender and the investor need from the builder.', cta, pb=px(m, 56, 32))
    stats = sec(t, m, stat_row(m, [('6', 'tax credit projects in progress'), ('677', 'units of 4% tax credit housing'), ('About $150M', 'bonding capacity'), ('5', 'projects under payment and performance bonds today')]),
                pt=0, pb=px(m, 88, 48))
    why = sec(t, m, head(m, 'What sponsors get', 'A builder that fits a tax credit closing') + f'<div style="height: {px(m,40,26)}px"></div>'
              + f'<div style="display: grid; grid-template-columns: repeat({px(m,2,1)}, minmax(0, 1fr)); gap: {px(m,"48px 56px","24px")}">' + ''.join(ruled(m, a, b) for a, b in AFF) + '</div>', bg=t['bg2'])
    rows = [(r[0], r[1], r[3], r[4]) for r in LIHTC]
    tbl = sec(t, m, head(m, 'In progress', 'Six tax credit projects, 677 units') + f'<div style="height: {px(m,40,24)}px"></div>'
              + table(m, [('Project', 'left'), ('Submarket', 'left'), ('Units', 'right'), ('Completion', 'right')], rows, total=('Six projects', '677 units', {0: 'Six projects', 2: '677'})))
    own = sec(t, m, f'<div style="display: grid; grid-template-columns: {px(m,"minmax(0, 1fr) minmax(0, 1fr)","minmax(0, 1fr)")}; gap: {px(m,64,28)}px; align-items: center">'
              f'<div>{head(m, "Owner and builder", "We sit on your side of the closing table too.")}<div style="height: 18px"></div>'
              f'<p style="margin: 0; font-size: {px(m,19,17)}px; line-height: 1.6; color: {MU}">2859 Francis Ave, 232 units in Koreatown, is a Six Peak 4% tax credit project, with LV as the builder. We have closed it as the sponsor, so we price and schedule yours as an owner would.</p>'
              f'<p style="margin: 16px 0 0; font-size: {px(m,19,17)}px; line-height: 1.6; color: {MU}">In select circumstances, {ext("Six Peak Capital")} provides credit enhancement and capital for projects.</p></div>'
              f'<div style="aspect-ratio: 4 / 3; background: #E2E7F0; display: flex; align-items: center; justify-content: center; text-align: center; padding: 20px; box-sizing: border-box; font-size: 15px; color: {MU}">[Rendering: 2859 Francis Ave, labeled as a rendering]</div></div>', bg=t['bg2'])
    nxt = sec(t, m, head(m, 'Awarded', 'Next: 206 units in Northridge', '8350 Reseda Blvd is a Six Peak joint venture: 206 units, all affordable, financed with 4% tax credits. LV Affordable Construction LP is the builder.')
              + f'<div style="height: {px(m,36,22)}px"></div>'
              + table(m, [('Project', 'left'), ('Submarket', 'left'), ('Units', 'right'), ('Stage', 'right')], [('8350 Reseda Blvd', 'Northridge', '206', 'Awarded, in preconstruction')]), pt=0)
    return ''.join([nav(m, 'afford'), hero, stats, why, tbl, nxt, own, gen.tom(t, m), gen.footer(t, m)])

# =================================================================== TEAM
LEAD_LV = [('Grady Lakamp', 'Founding Partner and CEO', '[Bio to come from Grady]'),
           ('Tom Taggart', 'Head of Business Development', '[Tom\'s approved bio]'),
           ('Pedro Rosales', 'Vice President', 'Leads construction operations: team development, project buyout, budget management and client relationships.')]
LEAD_SP = [('Chris Aiello', 'Founding Partner, Six Peak Capital', 'Co-founded Six Peak in 2016 in partnership with the Steyn Group. Leads Los Angeles acquisitions and development, and equity and debt capital markets.'),
           ('Bob Kennedy', 'Founding Partner, Six Peak Capital', 'Based in New York. Leads company operations and assists with tax credit and affordable housing execution.'),
           ('Justin Krueger', 'Founder and CEO, Icon National', 'Strategic partner to LV Construction.')]
BENCH = [('Operations and project management', [('Joe Lakamp', 'Executive Vice President'), ('Greg Smith', 'Executive Project Manager'), ('Dorian Puentes', 'Project Manager'),
                                                 ('Sammy Lozano', 'Assistant Project Manager'), ('Jonah Dobkin', 'Assistant Project Manager')]),
         ('Superintendents', [(n, 'Project Superintendent') for n in ['Roy Torres', 'Mike Savaikie', 'Daniel Carillo', 'Steven Garcia', 'Jesus Castellanos', 'Taylor Flores', 'Alex Rodriguez']]
          + [(n, 'Assistant Superintendent') for n in ['Nick Donald', 'Alfredo Tapia', 'Logan Terriquez']]),
         ('Field engineers', [(n, 'Field Engineer') for n in ['Albert Wolfe', 'Carlos Rocha', 'Ivan Delgado', 'Devis Tejada']]),
         ('Project coordination and office', [('Alina Akopians', 'Project Coordinator'), ('Brisa Sanchez', 'Project Coordinator'), ('Priscilla Hernandez', 'Project Coordinator'), ('Kim Moreno', 'Office Manager')]),
         ('Finance and development', [('Chris Andresen', 'Chief Financial Officer'), ('Robert Carrega', 'Controller'), ('Derek Sanders', 'Director of Development, Six Peak Capital')])]

def photo(name, small=False):
    key = 'team_' + name.lower().replace(' ', '-')
    if key in B:
        return f'<img src="{B[key]}" alt="{name}" style="display: block; width: 100%; aspect-ratio: 1 / 1; object-fit: cover">'
    return (f'<div style="aspect-ratio: 1 / 1; background: #E2E7F0; padding: 10px; box-sizing: border-box; display: flex; align-items: center; justify-content: center; text-align: center; '
            f'font-size: {12 if small else 14}px; line-height: 1.3; color: {MU}">[Photo: {name}]</div>')

def person(m, p):
    name, title, bio = p
    return (f'<div>{photo(name)}<div style="margin-top: 16px; font-family: {DISP}; font-weight: 600; font-size: 24px; color: {TX}">{name}</div>'
            f'<div style="font-size: 15px; font-weight: 600; color: {EB}; margin-top: 2px">{title}</div>'
            f'<p style="margin: 10px 0 0; font-size: 16px; line-height: 1.55; color: {MU}">{bio}</p></div>')

def bench_card(m, n, r):
    return (f'<div>{photo(n, small=True)}<div style="margin-top: 10px; font-weight: 600; font-size: 16px; line-height: 1.3; color: {TX}">{n}</div>'
            f'<div style="font-size: 14px; line-height: 1.35; color: {MU}">{r}</div></div>')

def page_team(m):
    hero = page_hero(m, 'Team', 'The people who would build your job.',
                     'LV Construction is led by Grady Lakamp, with Six Peak Capital partners Chris Aiello and Bob Kennedy and strategic partner Justin Krueger of Icon National. Preconstruction, estimating, project management, field supervision and accounting are all in-house.', pb=px(m, 56, 32))
    lv = sec(t, m, f'<div style="border-top: 2px solid {TX}; padding-top: 20px">{eyebrow(t, "LV Construction")}</div><div style="height: {px(m,32,22)}px"></div>'
             + grid(m, 3, ''.join(person(m, p) for p in LEAD_LV), gap=32, mgap=36), pt=0)
    sp = sec(t, m, f'<div style="border-top: 2px solid {TX}; padding-top: 20px">{eyebrow(t, "Six Peak Capital and strategic partner")}</div><div style="height: {px(m,32,22)}px"></div>'
             + grid(m, 3, ''.join(person(m, p) for p in LEAD_SP), gap=32, mgap=36)
             + f'<p style="margin: {px(m,36,24)}px 0 0; font-size: 16px; color: {MU}">LV Construction is the general contracting arm of {ext("Six Peak Capital")}.</p>', pt=0)
    groups = ''
    for g, people in BENCH:
        cards = ''.join(bench_card(m, n, r) for n, r in people)
        groups += (f'<div style="border-top: 1px solid {TX}; padding-top: 18px"><h3 style="margin: 0 0 20px; font-family: {DISP}; font-weight: 600; font-size: 21px; color: {TX}">{g}</h3>'
                   f'<div style="display: grid; grid-template-columns: repeat({px(m,6,2)}, minmax(0, 1fr)); gap: {px(m,"28px 24px","24px 16px")}">{cards}</div></div>')
    bench = sec(t, m, head(m, 'The bench', 'Who runs the work, in the office and in the field') + f'<div style="height: {px(m,40,26)}px"></div>'
                + f'<div style="display: flex; flex-direction: column; gap: {px(m,48,36)}px">{groups}</div>', bg=t['bg2'])
    return ''.join([nav(m, 'team'), hero, lv, sp, bench, gen.tom(t, m), gen.footer(t, m)])

# =================================================================== TALK TO TOM
def field(fid, label, typ='text', ph='', full=False, kind='input', opts=None):
    base = (f'width: 100%; box-sizing: border-box; min-height: 52px; padding: 12px 14px; border: 1.5px solid rgba(11,24,51,0.32); border-radius: 2px; background: #FFFFFF; '
            f'font-family: {FONT}; font-size: 17px; color: {TX}')
    lab = f'<label for="{fid}" style="display: block; font-size: 15px; font-weight: 600; color: {TX}; margin-bottom: 6px">{label}</label>'
    if kind == 'select':
        ctl = f'<select id="{fid}" style="{base}">' + ''.join(f'<option>{o}</option>' for o in opts) + '</select>'
    elif kind == 'textarea':
        ctl = f'<textarea id="{fid}" rows="4" placeholder="{ph}" style="{base}; resize: vertical"></textarea>'
    else:
        ctl = f'<input id="{fid}" type="{typ}" placeholder="{ph}" style="{base}">'
    return f'<div style="{"grid-column: 1 / -1; " if full else ""}">{lab}{ctl}</div>'

def page_contact(m):
    hero = page_hero(m, 'Contact us', 'Tell Tom what you are building.', 'Where it stands, and what you have drawn so far. No presentation and no pitch deck.', d=76, pb=px(m, 48, 28))
    form = (f'<form style="background: #FFFFFF; border: 1px solid {BD}; padding: {px(m,36,20)}px; display: grid; grid-template-columns: repeat({px(m,2,1)}, minmax(0, 1fr)); gap: 20px">'
            + field('f-name', 'Name') + field('f-co', 'Company') + field('f-email', 'Email', 'email') + field('f-phone', 'Phone', 'tel')
            + field('f-addr', 'Project address', full=True) + field('f-units', 'Approximate units')
            + field('f-stage', 'Where does the project stand?', kind='select', opts=['A site, nothing drawn', 'Entitlement set', 'Permit-ready drawings', 'A builder is already on'])
            + field('f-link', 'Link to the plan set, if you have one', 'url', full=True) + field('f-msg', 'Anything else Tom should know', kind='textarea', full=True)
            + f'<div style="grid-column: 1 / -1; display: flex; flex-wrap: wrap; gap: 16px; align-items: center">{btn(t, m, "Send to Tom", full=m)}'
            f'<span style="font-size: 15px; color: {MU}">It is free, and it is not a bid.</span></div></form>')
    ph = (f'<div style="width: 96px; height: 96px; flex: none; background: #E2E7F0; display: flex; align-items: center; justify-content: center; text-align: center; font-size: 12px; line-height: 1.3; color: {MU}; padding: 8px; box-sizing: border-box">[Photo: Tom Taggart]</div>')
    card = (f'<div style="display: flex; gap: 18px; align-items: center">{ph}<div><div style="font-family: {DISP}; font-weight: 600; font-size: 24px; color: {TX}">Tom Taggart</div>'
            f'<div style="font-size: 16px; color: {MU}">Head of Business Development</div></div></div>'
            f'<div style="margin-top: 18px; font-size: 17px; line-height: 1.8; color: {TX}"><div>[direct line]</div><div>[email]</div></div>'
            f'<div style="margin-top: 18px">{btn(t, m, "Book a call", primary=False, full=m)}</div>')
    nx = [('Tom replies', 'Within [response time].'), ('If you sent a set', 'You get our number within [two weeks]: total, per square foot and per unit, what we assumed, and the places it can move.'),
          ('No strings', 'It is free, and it is not a bid.')]
    nxt = ''.join(f'<li style="padding: 14px 0; border-top: 1px solid {BD}"><span style="display: block; font-weight: 600; font-size: 17px; color: {TX}">{a}</span><span style="display: block; font-size: 16px; line-height: 1.5; color: {MU}">{b}</span></li>' for a, b in nx)
    side = (f'<div><div style="border-top: 2px solid {TX}; padding-top: 24px">{card}</div>'
            f'<div style="margin-top: 40px">{eyebrow(t, "What happens next")}<ul style="list-style: none; margin: 14px 0 0; padding: 0">{nxt}</ul></div>'
            f'<div style="margin-top: 32px">{eyebrow(t, "Office")}<div style="margin-top: 10px; font-size: 16px; line-height: 1.6; color: {TX}">560 Riverdale Dr<br>Glendale, CA 91204</div></div></div>')
    body = sec(t, m, f'<div style="display: grid; grid-template-columns: {px(m,"minmax(0, 1.25fr) minmax(0, 0.75fr)","minmax(0, 1fr)")}; gap: {px(m,64,36)}px; align-items: start">{form}{side}</div>', pt=0)
    return ''.join([nav(m, None), hero, body, gen.footer(t, m)])

# =================================================================== HOME + PACKAGE (round 1 B, corrected)
def page_home(m):
    return ''.join([nav(m, None), gen.hero_home(t, m), gen.counters(t, m), gen.explainer(t, m), gen.projects(t, m, bg=t['bg2']), partnership(m), what_we_build(m, bg=t['bg2']),
                    gen.doors(t, m), gen.tom(t, m), gen.footer(t, m)])

def page_pkg(m):
    st = gen.steps(t, m, title='How your number was built', note=gen.NOTE_PKG, eb='Behind the number')
    pj = gen.projects(t, m, n=3, title='Three LV buildings closest to yours', eb='Who we are', intro=False, stats=False)
    return ''.join([nav(m, None), gen.hero_pkg(t, m), st, gen.isnot(t, m, bg=t['bg2']),
                    gen.explainer(t, m, compact=True, marker=True, title='When your number becomes a guarantee'), gen.nextsteps(t, m, bg=t['bg2']), pj, gen.tom(t, m), gen.footer(t, m, True)])

OPTIONS = [('A', 'Button links', 'Each page link is its own button on a white bar. The current page is filled navy.'),
           ('B', 'Navy tab band', 'Logo and Contact us on top, the five pages as full-width tabs below. The current page is underlined in rust.'),
           ('C', 'Navy bar', 'One navy bar with the logo on a light panel. The current page is underlined.')]

def page_banner(m):
    """One board that shows the three banner designs side by side, desktop and phone. Same words on each."""
    skel = lambda w: (f'<div style="background: {t["bg"]}; padding: 26px 0 30px">' + wrap(w, f'<div style="height: 12px; width: {px(w, 180, 130)}px; background: rgba(168,74,21,0.30)"></div>'
                      f'<div style="height: {px(w, 30, 22)}px; width: {px(w, 620, 300)}px; max-width: 100%; background: rgba(11,24,51,0.14); margin-top: 16px"></div>'
                      f'<div style="height: {px(w, 30, 22)}px; width: {px(w, 440, 220)}px; max-width: 100%; background: rgba(11,24,51,0.14); margin-top: 10px"></div>') + '</div>')
    def tag(letter, name, why, small=False):
        used = (f'<span style="display: inline-flex; align-items: center; min-height: 26px; padding: 0 10px; background: {RUST}; color: #FFFFFF; font-size: 13px; font-weight: 700; '
                f'letter-spacing: 0.04em; border-radius: 2px">On every page in this round</span>') if letter == NAV_STYLE else ''
        if small:
            return (f'<div style="display: flex; align-items: baseline; gap: 10px; margin-bottom: 12px"><span style="font-family: {DISP}; font-weight: 700; font-size: 22px; color: {TX}">{letter}</span>'
                    f'<span style="font-size: 16px; font-weight: 600; color: {TX}">{name}</span></div>')
        return (f'<div style="display: flex; flex-wrap: wrap; align-items: center; gap: 8px 18px; padding: 0 0 16px"><span style="font-family: {DISP}; font-weight: 700; font-size: 34px; line-height: 1; color: {TX}">{letter}</span>'
                f'<span style="font-family: {DISP}; font-weight: 600; font-size: 24px; color: {TX}">{name}</span>{used}'
                f'<span style="flex-basis: 100%; font-size: 16px; color: {MU}">{why}</span></div>')
    top = sec(t, False, f'{eyebrow(t, "Banner options")}<div style="height: 14px"></div>{h2(t, False, "Three designs for the banner. The words are the same on each.", 900)}'
              f'<div style="height: 16px"></div>{lead(t, False, "Each is shown as it looks on the Projects page. The links change color when the pointer is over them. Name a letter and every page takes that banner.", 820)}',
              bg='#FFFFFF', pt=64, pb=24)
    rows = ''
    for letter, name, why in OPTIONS:
        rows += (f'<div style="background: #FFFFFF; padding: 36px 0 0">{wrap(False, tag(letter, name, why))}</div>'
                 f'<div style="border-top: 1px solid {BD}; border-bottom: 1px solid {BD}">{nav(False, "projects", style=letter)}{skel(False)}</div>')
    frames = ''
    for letter, name, why in OPTIONS:
        frames += (f'<div style="width: 390px; flex: none">{tag(letter, name, why, small=True)}'
                   f'<div style="border: 1px solid {BD}">{nav(True, "projects", style=letter)}{skel(True)}</div></div>')
    phones = (f'<div style="background: #FFFFFF; padding: 48px 0 64px"><div style="width: 1230px; margin: 0 auto">'
              f'<div style="font-family: {DISP}; font-weight: 600; font-size: 24px; color: {TX}; margin-bottom: 20px">On a phone</div>'
              f'<div style="display: flex; gap: 30px; align-items: flex-start">{frames}</div></div></div>')
    return top + rows + phones

PAGES = [('Home', 'Homepage', page_home), ('Package', 'Package landing page', page_pkg), ('HowWePrice', 'How we price', page_price), ('RomToGmp', 'ROM to GMP', page_gmp),
         ('Projects', 'Projects', page_projects), ('Project_Reading', 'Project page (Reading)', page_project), ('Affordable', 'Affordable housing', page_afford),
         ('Team', 'Team', page_team), ('TalkToTom', 'Contact us', page_contact)]
BOARDS = []
for key, name, fn in PAGES:
    for dev in ('Desktop', 'Phone'):
        f = 'Main.dc.html' if (key, dev) == ('Home', 'Desktop') else f'{key}_{dev}.dc.html'
        BOARDS.append((f, f'{name}, {dev.lower()}', key, name, dev == 'Phone', fn))
BOARDS.append(('Banner_Options.dc.html', 'Banner options', 'Banner', 'Banner options', False, page_banner))

def build(heights):
    os.makedirs(OUT, exist_ok=True)
    for f, title, key, name, m, fn in BOARDS:
        body = re.sub(r'<div style="width: (\d+)px; height: \d+px; flex: none;[^"]*">\[Photo: Tom Taggart\]</div>',
                      lambda mo: f'<img src="{B["team_tom-taggart"]}" alt="Tom Taggart" style="width: {mo.group(1)}px; height: {mo.group(1)}px; flex: none; object-fit: cover; display: block">', fn(m))
        assert '[Photo: Tom Taggart]' not in body, f
        body = wire(body, m)
        open(os.path.join(OUT, f), 'w', encoding='utf-8').write(gen.doc(t, title, body, 390 if m else 1440, heights.get(f, 3000), css=NAV_CSS))

def canvas(heights):
    boards, order, notes = {}, [], {}
    rows = [PAGES[:5], PAGES[5:]]
    y = 0
    for r, row in enumerate(rows):
        x = 0
        rowh = 0
        for key, name, fn in row:
            fd = 'Main.dc.html' if key == 'Home' else f'{key}_Desktop.dc.html'
            fp = f'{key}_Phone.dc.html'
            boards[fd] = {"x": x, "y": y, "w": 1440, "h": heights[fd], "title": f'{name}, desktop', "expand": "fill", "is_interactive": True}
            boards[fp] = {"x": x + 1520, "y": y, "w": 390, "h": heights[fp], "title": f'{name}, phone', "expand": "fill", "is_interactive": True}
            order += [fd, fp]
            notes[f'n_{key}'] = {"x": x, "y": y - 300, "text": name, "kind": "title1", "maxW": 1910}
            rowh = max(rowh, heights[fd], heights[fp])
            x += 2150
        y += rowh + 420
    fo = 'Banner_Options.dc.html'
    boards[fo] = {"x": -1700, "y": 0, "w": 1440, "h": heights[fo], "title": 'Banner options', "expand": "fill", "is_interactive": True}
    order.insert(0, fo)
    notes['n_Banner'] = {"x": -1700, "y": -300, "text": 'Banner options', "kind": "title1", "maxW": 1440}
    idx = {"v": 3, "createdOnFiles": {"v": 1, "at": "2026-11-19T00:50:00Z"}, "title": "LV website mockups: round 2 (Light editorial)",
           "launch": {"view": "canvas"}, "pages": [], "boards": boards, "order": order, "notes": notes, "designSystems": []}
    json.dump(idx, open(os.path.join(OUT, 'canvas.json'), 'w', encoding='utf-8'), indent=1)

if __name__ == '__main__':
    hp = '/home/claude/lvmock/heights2.json'
    heights = json.load(open(hp)) if os.path.exists(hp) else {}
    build(heights)
    if heights:
        canvas(heights)
    print('built', len(BOARDS), 'boards; heights known:', bool(heights))
