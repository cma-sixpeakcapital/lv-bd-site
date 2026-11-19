#!/usr/bin/env python3
"""Generates the round 1 LV website mockups: 3 directions x 2 pages x 2 widths."""
import json, os, re, sys

OUT = '/home/claude/lvmock/root/project'
BLOB = {
    'berry': '/_blob/ebb1344bde70cd41d340543348cfd58a',
    'berry2': '/_blob/e2561e771434f7d7c8da25f9c8caea24',
    'reading': '/_blob/765ecb7cdffd9652ee7f5873365e0463',
    'wilton': '/_blob/00c3dfda1b7ae06537ad9205b25f27aa',
    'venice': '/_blob/34c93132f352865951f48bd82d98c270',
    'roof': '/_blob/3cc1e8cfd7e0daddfe4eeb412a2d027a',
    'logo': '/_blob/1e6e65e65894ed2554542936c164b2fa',
}
FONT = "'Inter','Segoe UI',system-ui,sans-serif"
DISP = "'DM Sans','Inter','Segoe UI',sans-serif"
RUST = '#C4581A'

T = {
 'A': dict(k='A', name='Pitchbook dark', bg='#0B1833', bg2='#111E3D', surface='#1E2C44', text='#F8F9F4',
           muted='#BFC7DA', fine='#94A3B8', border='rgba(191,199,218,0.18)', eyebrow='#E8935A', accent='#E8935A',
           no='#BFC7DA', notyet='#E8A84C', yes='#E8935A', band='rgba(142,163,190,0.30)', line='#E8935A',
           r=12, rb=8, link='#E8935A', linkh='#F8F9F4', pillbg='#F8F9F4', pilltx='#0B1833',
           foot='#111E3D', foottx='#BFC7DA', ph='#2C3A51'),
 'B': dict(k='B', name='Light editorial', bg='#FAFAF6', bg2='#FFFFFF', surface='#FFFFFF', text='#0B1833',
           muted='#475569', fine='#475569', border='rgba(11,24,51,0.16)', eyebrow='#A84A15', accent=RUST,
           no='#475569', notyet='#9A6A12', yes=RUST, band='rgba(184,199,216,0.60)', line=RUST,
           r=0, rb=2, link='#A84A15', linkh='#0B1833', pillbg='#0B1833', pilltx='#F8F9F4',
           foot='#FAFAF6', foottx='#475569', ph='#E2E7F0'),
 'C': dict(k='C', name='Data-forward', bg='#E2E7F0', bg2='#F4F6FA', surface='#FFFFFF', text='#0B1833',
           muted='#475569', fine='#475569', border='rgba(11,24,51,0.10)', eyebrow='#A84A15', accent=RUST,
           no='#475569', notyet='#9A6A12', yes=RUST, band='rgba(142,163,190,0.40)', line=RUST,
           r=12, rb=8, link='#A84A15', linkh='#0B1833', pillbg='#0B1833', pilltx='#F8F9F4',
           foot='#0B1833', foottx='#BFC7DA', ph='#E2E7F0'),
}

# ------------------------------------------------------------------ atoms
def px(m, d, p):
    return p if m else d

def cnt(n):
    """Mark a figure to count up when it scrolls into view (site.js). Years and words are left alone."""
    n = str(n)
    if re.fullmatch(r'(19|20)\d\d', n) or not re.search(r'\d', n):
        return n
    return f'<span data-count style="font-variant-numeric: tabular-nums">{n}</span>'

def wrap(m, inner, extra=''):
    return f'<div style="max-width: 1200px; margin: 0 auto; padding: 0 {px(m,80,20)}px; box-sizing: border-box; {extra}">{inner}</div>'

def sec(t, m, inner, bg=None, pt=None, pb=None, extra=''):
    pt = px(m, 96, 56) if pt is None else pt
    pb = px(m, 96, 56) if pb is None else pb
    b = f'background: {bg}; ' if bg else ''
    return f'<section style="{b}padding: {pt}px 0 {pb}px; {extra}">{wrap(m, inner)}</section>'

def eyebrow(t, text, color=None):
    return f'<div style="font-size: 13px; font-weight: 700; letter-spacing: 0.2em; text-transform: uppercase; color: {color or t["eyebrow"]}">{text}</div>'

def h2(t, m, text, mw=820):
    return f'<h2 style="margin: 0; font-family: {DISP}; font-weight: 600; font-size: {px(m,44,30)}px; line-height: 1.1; letter-spacing: -0.01em; text-wrap: balance; color: {t["text"]}; max-width: {mw}px">{text}</h2>'

def lead(t, m, text, mw=680):
    return f'<p style="margin: 0; font-size: {px(m,19,17)}px; line-height: 1.55; color: {t["muted"]}; max-width: {mw}px">{text}</p>'

def btn(t, m, label, primary=True, small=False, full=False):
    h = 44 if small else 54
    w = 'width: 100%; box-sizing: border-box; ' if full else ''
    if primary:
        return (f'<a href="#" style="{w}display: inline-flex; align-items: center; justify-content: center; min-height: {h}px; padding: 0 {18 if small else 28}px; '
                f'background: {RUST}; color: #FFFFFF; font-weight: 700; font-size: 19px; border-radius: {t["rb"]}px; text-decoration: none; white-space: nowrap">{label}</a>')
    return (f'<a href="#" style="{w}display: inline-flex; align-items: center; justify-content: center; min-height: {h}px; padding: 0 {18 if small else 26}px; '
            f'border: 1.5px solid {t["text"]}; color: {t["text"]}; font-weight: 600; font-size: 17px; border-radius: {t["rb"]}px; text-decoration: none; box-sizing: border-box">{label}</a>')

def textlink(t, label):
    return f'<a href="#" style="display: inline-flex; align-items: center; min-height: 44px; font-weight: 600; font-size: 16px; color: {t["link"]}; text-decoration: underline; text-underline-offset: 4px">{label}</a>'

def logo(t, m, panel=False, h=None):
    h = h or px(m, 46, 36)
    img = f'<img src="{BLOB["logo"]}" alt="LV Construction" style="height: {h}px; width: auto; display: block">'
    if panel:
        return f'<div style="background: #F8F9F4; padding: 10px 14px; border-radius: 6px; display: inline-block">{img}</div>'
    return img

MENU_ICON = ('<svg aria-hidden="true" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round">'
             '<path d="M4 7h16M4 12h16M4 17h16"></path></svg>')

def icon(path, color, size=28):
    return (f'<svg aria-hidden="true" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="1.6" '
            f'stroke-linecap="round" stroke-linejoin="round">{path}</svg>')

IC_PLANS = '<path d="M6 3h9l4 4v14H6z"></path><path d="M15 3v4h4"></path><path d="M9 12h7M9 16h7"></path>'
IC_SHIELD = '<path d="M12 3l7 3v6c0 4.5-3 7.5-7 9-4-1.5-7-4.5-7-9V6z"></path><path d="M9 12l2 2 4-4"></path>'
IC_PIN = '<path d="M12 21s-6-5.5-6-10a6 6 0 1112 0c0 4.5-6 10-6 10z"></path><circle cx="12" cy="11" r="2"></circle>'
IC_CHECK = '<path d="M5 12.5l4.5 4.5L19 7.5"></path>'
IC_X = '<path d="M6 6l12 12M18 6L6 18"></path>'
IC_PLAY = '<circle cx="12" cy="12" r="9"></circle><path d="M10 8.5v7l6-3.5z"></path>'

# ------------------------------------------------------------------ nav
def nav(t, m, minimal=False):
    k = t['k']
    links = ['How we price', 'ROM to GMP', 'Projects', 'Affordable housing', 'Team']
    lg = logo(t, m, panel=(k == 'A'))
    right = btn(t, m, 'Talk to Tom', small=True)
    if m:
        menu = '' if minimal else (f'<button type="button" aria-label="Menu" style="width: 44px; height: 44px; display: inline-flex; align-items: center; justify-content: center; '
                                   f'background: transparent; border: 1.5px solid {t["border"]}; border-radius: {t["rb"]}px; color: {t["text"]}">{MENU_ICON}</button>')
        inner = f'<div style="display: flex; align-items: center; justify-content: space-between; gap: 12px; min-height: 72px">{lg}<div style="display: flex; gap: 10px; align-items: center">{right}{menu}</div></div>'
    else:
        mid = '' if minimal else ('<nav aria-label="Main" style="display: flex; gap: 34px">' + ''.join(
            f'<a href="#" style="display: inline-flex; align-items: center; min-height: 44px; font-size: 16px; font-weight: 500; color: {t["text"]}; text-decoration: none">{l}</a>' for l in links) + '</nav>')
        inner = f'<div style="display: flex; align-items: center; justify-content: space-between; gap: 24px; min-height: 92px">{lg}{mid}{right}</div>'
    bg = {'A': t['bg'], 'B': t['bg'], 'C': '#FFFFFF'}[k]
    rule = f'border-bottom: 1px solid {t["border"]}; ' if k in ('B', 'C') else ''
    stripe = f'<div style="height: 6px; background: {RUST}"></div>' if k == 'A' else ''
    return f'{stripe}<header style="background: {bg}; {rule}">{wrap(m, inner)}</header>'

# ------------------------------------------------------------------ cost band
STAGES = [
    ('ROM', 'ROM', 'From early plans and our own bid history. A budget for underwriting.', 'No', 'no'),
    ('Precon updates', 'Precon', 'As the drawings develop, we update the estimate from the new plans, with early trade pricing where it helps.', 'No', 'no'),
    ('Hard bid', 'Hard bid', 'With a closing and a start date in sight, the job goes to the trades for hard bids. Real prices, good for a limited time.', 'Not yet', 'notyet'),
    ('GMP', 'GMP', 'Hard bids in hand and a verified start date. Now LV commits.', 'Yes', 'yes'),
]

def band_svg(t, h=150):
    return (f'<svg role="img" aria-label="The cost range narrows from ROM to GMP, where it becomes one guaranteed number" viewBox="0 0 1000 200" preserveAspectRatio="none" '
            f'style="display: block; width: 100%; height: {h}px">'
            f'<polygon points="0,8 250,44 500,74 750,94 750,106 500,126 250,156 0,192" fill="{t["band"]}"></polygon>'
            f'<line x1="750" y1="100" x2="1000" y2="100" stroke="{t["line"]}" stroke-width="6" vector-effect="non-scaling-stroke"></line>'
            + ''.join(f'<line x1="{x}" y1="0" x2="{x}" y2="200" stroke="{t["border"]}" stroke-width="1" vector-effect="non-scaling-stroke"></line>' for x in (250, 500, 750))
            + '</svg>')

def stages(t, m, compact=False, marker=False, h=150):
    pill = (f'<div style="display: inline-block; background: {t["pillbg"]}; color: {t["pilltx"]}; font-size: 13px; font-weight: 700; padding: 6px 12px; border-radius: 999px; white-space: nowrap">Your number is here</div>')
    if m:
        widths = ['100%', '66%', '36%']
        rows = ''
        for i, (name, sub, desc, ans, key) in enumerate(STAGES):
            bar = (f'<div style="height: 4px; background: {t["line"]}; width: 100%"></div>' if i == 3 else
                   f'<div style="height: 14px; background: {t["band"]}; width: {widths[i]}; margin: 0 auto"></div>')
            mk = f'<div style="margin-bottom: 10px">{pill}</div>' if (marker and i == 0) else ''
            d = '' if compact else f'<div style="font-size: 15px; line-height: 1.5; color: {t["muted"]}; margin-top: 4px">{desc}</div>'
            rows += (f'<div style="padding: 18px 0; border-top: 1px solid {t["border"]}">{mk}'
                     f'<div style="display: flex; justify-content: space-between; align-items: baseline; gap: 12px">'
                     f'<div style="font-family: {DISP}; font-weight: 600; font-size: 21px; color: {t["text"]}">{name}</div>'
                     f'<div style="font-size: 14px; color: {t["muted"]}; white-space: nowrap">Guaranteed? <span style="font-weight: 700; font-size: 19px; color: {t[key]}">{ans}</span></div></div>'
                     f'{d}<div style="margin-top: 14px">{bar}</div></div>')
        return f'<div>{rows}</div>'
    mk = (f'<div style="display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); margin-bottom: 10px"><div>{pill}</div></div>' if marker else '')
    cells = ''
    for i, (name, sub, desc, ans, key) in enumerate(STAGES):
        d = '' if compact else f'<div style="font-size: 15px; line-height: 1.5; color: {t["muted"]}; margin-top: 8px">{desc}</div>'
        cells += (f'<div style="padding: 18px 24px 0 0; display: flex; flex-direction: column">'
                  f'<div style="font-size: 13px; font-weight: 600; color: {t["muted"]}">Stage {i+1}</div>'
                  f'<div style="font-family: {DISP}; font-weight: 600; font-size: {20 if compact else 24}px; color: {t["text"]}; margin-top: 2px">{sub if compact else name}</div>'
                  f'{d}'
                  f'<div style="margin-top: auto; padding-top: 14px"><div style="font-size: 14px; color: {t["muted"]}">Guaranteed?</div>'
                  f'<div style="font-family: {DISP}; font-weight: 700; font-size: {24 if compact else 28}px; color: {t[key]}">{ans}</div></div></div>')
    return f'{mk}{band_svg(t, h)}<div style="display: grid; grid-template-columns: repeat(4, minmax(0, 1fr))">{cells}</div>'

ONE_LINE = 'A ROM is a budget. A GMP is a guarantee. The guarantee takes hard bids and a verified start date.'

def explainer(t, m, compact=False, marker=False, bg=None, title='When does a construction number become a guarantee?'):
    head = (f'{eyebrow(t, "ROM to GMP")}<div style="height: 14px"></div>{h2(t, m, title)}<div style="height: 16px"></div>'
            + lead(t, m, 'A project is priced again and again on the way to construction. Only the last number is guaranteed.'))
    close = (f'<div style="margin-top: {px(m,48,32)}px; display: flex; flex-wrap: wrap; gap: 24px; align-items: center; justify-content: space-between; '
             f'border-top: 1px solid {t["border"]}; padding-top: {px(m,32,24)}px">'
             f'<div style="font-family: {DISP}; font-weight: 600; font-size: {px(m,26,21)}px; line-height: 1.25; color: {t["text"]}; max-width: 720px">{ONE_LINE}</div>'
             f'<a href="#" style="display: inline-flex; align-items: center; gap: 10px; min-height: 54px; padding: 0 24px; border: 1.5px solid {t["text"]}; color: {t["text"]}; '
             f'font-weight: 600; font-size: 17px; border-radius: {t["rb"]}px; text-decoration: none; box-sizing: border-box">{icon(IC_PLAY, t["text"], 22)}Watch the one-minute explainer</a></div>')
    body = f'{head}<div style="height: {px(m,48,28)}px"></div>{stages(t, m, compact, marker)}{"" if compact else close}'
    return sec(t, m, body, bg=bg)

# ------------------------------------------------------------------ library counters
COUNTERS = [('$270M', 'of Los Angeles multifamily work in the cost library'), ('451', 'bought-out trade lines'),
            ('33', 'trades'), ('15', 'projects, completed and in construction')]
ASOF = 'Library as of 19 October 2026. Refreshed every quarter.'

def counters(t, m):
    k = t['k']
    if k == 'A':
        cells = ''.join(
            f'<div><div style="font-family: {DISP}; font-weight: 700; font-size: {px(m,48,36)}px; line-height: 1; color: {t["accent"] if i == 0 else t["text"]}">{n}</div>'
            f'<div style="margin-top: 10px; font-size: 15px; line-height: 1.4; color: {t["muted"]}">{l}</div></div>' for i, (n, l) in enumerate(COUNTERS))
        body = (f'{eyebrow(t, "The cost library behind every number")}<div style="height: {px(m,28,22)}px"></div>'
                f'<div style="display: grid; grid-template-columns: repeat({px(m,4,2)}, minmax(0, 1fr)); gap: {px(m,40,28)}px">{cells}</div>'
                f'<div style="margin-top: {px(m,28,22)}px; font-size: 13px; color: {t["fine"]}">{ASOF}</div>')
        return sec(t, m, body, bg=t['bg2'], pt=px(m, 56, 40), pb=px(m, 56, 40))
    if k == 'B':
        cells = ''
        for i, (n, l) in enumerate(COUNTERS):
            bl = '' if (i == 0 or (m and i % 2 == 0)) else f'border-left: 1px solid {t["border"]}; padding-left: {px(m,32,18)}px; '
            cells += (f'<div style="{bl}"><div style="font-family: {DISP}; font-weight: 600; font-size: {px(m,60,40)}px; line-height: 1; letter-spacing: -0.02em; color: {t["accent"] if i == 0 else t["text"]}">{cnt(n)}</div>'
                      f'<div style="margin-top: 12px; font-size: 15px; line-height: 1.4; color: {t["muted"]}">{l}</div></div>')
        body = (f'<div style="border-top: 2px solid {t["text"]}; padding-top: 20px; display: flex; justify-content: space-between; flex-wrap: wrap; gap: 8px">'
                f'{eyebrow(t, "The cost library behind every number")}<div style="font-size: 13px; color: {t["fine"]}">{ASOF}</div></div>'
                f'<div style="height: {px(m,36,24)}px"></div>'
                f'<div style="display: grid; grid-template-columns: repeat({px(m,4,2)}, minmax(0, 1fr)); gap: {px(m,32,24)}px">{cells}</div>')
        return sec(t, m, body, pt=px(m, 72, 44), pb=px(m, 24, 12))
    cells = ''.join(
        f'<div style="background: #FFFFFF; border: 1px solid {t["border"]}; border-radius: 12px; padding: {px(m,24,18)}px">'
        f'<div style="font-family: {DISP}; font-weight: 700; font-size: {px(m,44,34)}px; line-height: 1; font-variant-numeric: tabular-nums; color: {t["accent"] if i == 0 else t["text"]}">{n}</div>'
        f'<div style="margin-top: 10px; font-size: 14px; line-height: 1.4; color: {t["muted"]}">{l}</div></div>' for i, (n, l) in enumerate(COUNTERS))
    body = (f'<div style="display: flex; justify-content: space-between; flex-wrap: wrap; gap: 8px; align-items: baseline">{eyebrow(t, "The cost library behind every number")}'
            f'<div style="font-size: 13px; color: {t["fine"]}">{ASOF}</div></div><div style="height: 18px"></div>'
            f'<div style="display: grid; grid-template-columns: repeat({px(m,4,2)}, minmax(0, 1fr)); gap: {px(m,20,12)}px">{cells}</div>')
    return sec(t, m, body, pt=0, pb=px(m, 72, 44))

# ------------------------------------------------------------------ three doors
DOORS = [
    ('Plans on file', 'Send the set, at whatever stage it is. You get our number: total, per square foot and per unit, what we assumed, and the places it can move.', 'Send a plan set', IC_PLANS),
    ('A tax credit deal', 'Six 4% tax credit projects in progress, 677 units. We bond the job and know the lender and investor process.', 'Affordable housing', IC_SHIELD),
    ('A site you just bought', 'Before you settle on a scheme, see what wood-frame apartment buildings are costing us this quarter, trade by trade.', 'Ask for the cost sheet', IC_PIN),
]

def doors(t, m, bg=None):
    k = t['k']
    cards = ''
    for i, (title, text, link, ic) in enumerate(DOORS):
        if k == 'A':
            cards += (f'<div style="background: {t["surface"]}; border-radius: 12px; padding: {px(m,32,24)}px; display: flex; flex-direction: column; gap: 14px">'
                      f'<div style="width: 40px; height: 4px; background: {RUST}"></div>'
                      f'<h3 style="margin: 0; font-family: {DISP}; font-weight: 600; font-size: 24px; color: {t["text"]}">{title}</h3>'
                      f'<p style="margin: 0; font-size: 16px; line-height: 1.55; color: {t["muted"]}">{text}</p><div>{textlink(t, link)}</div></div>')
        elif k == 'B':
            cards += (f'<div style="border-top: 2px solid {t["text"]}; padding-top: 20px; display: flex; flex-direction: column; gap: 14px">'
                      f'<div style="font-size: 13px; font-weight: 700; letter-spacing: 0.2em; color: {t["eyebrow"]}">0{i+1}</div>'
                      f'<h3 style="margin: 0; font-family: {DISP}; font-weight: 600; font-size: 28px; line-height: 1.15; color: {t["text"]}">{title}</h3>'
                      f'<p style="margin: 0; font-size: 17px; line-height: 1.55; color: {t["muted"]}">{text}</p><div>{textlink(t, link)}</div></div>')
        else:
            cards += (f'<div style="background: #FFFFFF; border: 1px solid {t["border"]}; border-radius: 12px; padding: {px(m,28,22)}px; display: flex; flex-direction: column; gap: 12px">'
                      f'{icon(ic, t["eyebrow"], 30)}'
                      f'<h3 style="margin: 0; font-family: {DISP}; font-weight: 600; font-size: 22px; color: {t["text"]}">{title}</h3>'
                      f'<p style="margin: 0; font-size: 16px; line-height: 1.55; color: {t["muted"]}">{text}</p><div>{textlink(t, link)}</div></div>')
    body = (f'{eyebrow(t, "Start here")}<div style="height: 14px"></div>{h2(t, m, "Where is your project today?")}<div style="height: {px(m,40,26)}px"></div>'
            f'<div style="display: grid; grid-template-columns: repeat({px(m,3,1)}, minmax(0, 1fr)); gap: {px(m,28,18 if k != "B" else 32)}px">{cards}</div>')
    return sec(t, m, body, bg=bg)

# ------------------------------------------------------------------ process steps
STEPS = [('Read the plans', 'Schedules, sections and code areas set every budget-driving input.'),
         ('Price each line', 'Our committed rate for the trade, times your quantity.'),
         ('Apply scope drivers', 'Parking, podium, HVAC, finish level and labor terms, set from your design.'),
         ('Clarify and issue', 'Open items go back to you to confirm before the number is final.')]

def steps(t, m, title='How we price a building', note=None, bg=None, eb='How we price'):
    k = t['k']
    cells = ''
    for i, (a, b) in enumerate(STEPS):
        num = f'<div style="font-family: {DISP}; font-weight: 700; font-size: 18px; color: {t["eyebrow"]}">0{i+1}</div>'
        ttl = f'<h3 style="margin: 0; font-family: {DISP}; font-weight: 600; font-size: 21px; color: {t["text"]}">{a}</h3>'
        txt = f'<p style="margin: 0; font-size: 16px; line-height: 1.5; color: {t["muted"]}">{b}</p>'
        if k == 'A':
            box = f'background: {t["surface"]}; border-radius: 12px; padding: 24px; '
        elif k == 'B':
            box = f'border-top: 1px solid {t["text"]}; padding-top: 18px; '
        else:
            box = f'background: #FFFFFF; border: 1px solid {t["border"]}; border-radius: 12px; padding: 22px; '
        cells += f'<div style="{box}display: flex; flex-direction: column; gap: 10px">{num}{ttl}{txt}</div>'
    n = f'<div style="margin-top: {px(m,28,20)}px; font-size: 16px; color: {t["muted"]}">{note}</div>' if note else ''
    body = (f'{eyebrow(t, eb)}<div style="height: 14px"></div>{h2(t, m, title)}<div style="height: {px(m,40,26)}px"></div>'
            f'<div style="display: grid; grid-template-columns: repeat({px(m,4,1)}, minmax(0, 1fr)); gap: {px(m,24,14)}px">{cells}</div>{n}')
    return sec(t, m, body, bg=bg)

# ------------------------------------------------------------------ projects
PROJ = [('Berryman I', 'Mar Vista', '156 leasable units', 'Delivered 2025', 'berry', 'Berryman I at dusk, seen from above'),
        ('Reading', 'Westchester', '124 leasable units', 'Delivered 2025', 'reading', 'Reading, a five-story blue and white building'),
        ('Wilton', 'Los Angeles', '132 leasable units', 'Delivered 2026', 'wilton', 'Wilton, seen from the street corner'),
        ('Venice', 'Mar Vista', '112 leasable units', 'Delivered 2023', 'venice', 'Venice, a four-story white and black building')]
TRACK = [('8', 'buildings completed since 2020'), ('10', 'under construction, 927 units'),
         ('About $150M', 'bonding capacity for affordable and tax credit work')]

def pcard(t, m, p, ratio='4 / 3', big=False):
    name, hood, units, dlv, key, alt = p
    r = t['r']
    return (f'<div><img src="{BLOB[key]}" alt="{alt}" style="display: block; width: 100%; aspect-ratio: {ratio}; object-fit: cover; border-radius: {r}px">'
            f'<div style="margin-top: 14px; font-family: {DISP}; font-weight: 600; font-size: {26 if big and not m else 21}px; color: {t["text"]}">{name}</div>'
            f'<div style="margin-top: 2px; font-size: 15px; color: {t["muted"]}">{hood} | {units} | {dlv}</div></div>')

def trackstats(t, m):
    k = t['k']
    cells = ''
    for i, (n, l) in enumerate(TRACK):
        if k == 'C':
            cells += (f'<div style="background: #FFFFFF; border: 1px solid {t["border"]}; border-radius: 12px; padding: 20px">'
                      f'<div style="font-family: {DISP}; font-weight: 700; font-size: {px(m,34,28)}px; line-height: 1.05; color: {t["text"]}">{n}</div>'
                      f'<div style="margin-top: 8px; font-size: 14px; line-height: 1.4; color: {t["muted"]}">{l}</div></div>')
        else:
            bt = f'border-top: 1px solid {t["border"]}; padding-top: 16px; '
            cells += (f'<div style="{bt}"><div style="font-family: {DISP}; font-weight: 600; font-size: {px(m,38,30)}px; line-height: 1.05; color: {t["text"]}">{cnt(n)}</div>'
                      f'<div style="margin-top: 8px; font-size: 15px; line-height: 1.4; color: {t["muted"]}">{l}</div></div>')
    return f'<div style="display: grid; grid-template-columns: repeat({px(m,3,1)}, minmax(0, 1fr)); gap: {px(m,28,16)}px">{cells}</div>'

def projects(t, m, bg=None, n=4, title='We built for ourselves first.', eb='Track record', intro=True, stats=True):
    k = t['k']
    ps = PROJ[:n]
    head = f'{eyebrow(t, eb)}<div style="height: 14px"></div>{h2(t, m, title)}'
    if intro:
        head += '<div style="height: 16px"></div>' + lead(t, m, 'Six Peak developed these buildings and LV built them. That owner-builder history is where the cost discipline on third-party work comes from.')
    if k == 'C':
        rows = ''
        for i, (name, hood, units, dlv, key, alt) in enumerate(ps):
            bt = '' if i == 0 else f'border-top: 1px solid {t["border"]}; '
            if m:
                rows += (f'<div style="{bt}display: flex; gap: 14px; align-items: center; padding: 14px 0">'
                         f'<img src="{BLOB[key]}" alt="{alt}" style="width: 96px; height: 72px; object-fit: cover; border-radius: 8px; flex: none">'
                         f'<div><div style="font-family: {DISP}; font-weight: 600; font-size: 19px; color: {t["text"]}">{name}</div>'
                         f'<div style="font-size: 14px; color: {t["muted"]}">{hood} | {units}</div><div style="font-size: 14px; color: {t["muted"]}">{dlv}</div></div></div>')
            else:
                rows += (f'<div style="{bt}display: grid; grid-template-columns: 132px minmax(0, 1.4fr) minmax(0, 1fr) minmax(0, 1fr) minmax(0, 1fr); gap: 24px; align-items: center; padding: 14px 0">'
                         f'<img src="{BLOB[key]}" alt="{alt}" style="width: 132px; height: 88px; object-fit: cover; border-radius: 8px">'
                         f'<div style="font-family: {DISP}; font-weight: 600; font-size: 21px; color: {t["text"]}">{name}</div>'
                         f'<div style="font-size: 16px; color: {t["muted"]}">{hood}</div>'
                         f'<div style="font-size: 16px; color: {t["text"]}; font-variant-numeric: tabular-nums">{units}</div>'
                         f'<div style="font-size: 16px; color: {t["muted"]}">{dlv}</div></div>')
        grid = f'<div style="background: #FFFFFF; border: 1px solid {t["border"]}; border-radius: 12px; padding: {px(m,"10px 28px","4px 18px")}">{rows}</div>'
    elif k == 'B' and n == 4:
        grid = (f'<div style="display: grid; grid-template-columns: repeat({px(m,2,1)}, minmax(0, 1fr)); gap: {px(m,"56px 40px","32px")}">'
                + ''.join(pcard(t, m, p, '3 / 2', big=True) for p in ps) + '</div>')
    else:
        grid = (f'<div style="display: grid; grid-template-columns: repeat({px(m,n,1)}, minmax(0, 1fr)); gap: {px(m,28,28)}px">'
                + ''.join(pcard(t, m, p) for p in ps) + '</div>')
    st = f'<div style="height: {px(m,40,28)}px"></div>{trackstats(t, m)}' if stats else ''
    more = f'<div style="margin-top: {px(m,32,20)}px">{textlink(t, "All projects")}</div>' if n == 4 else ''
    body = f'{head}{st}<div style="height: {px(m,44,28)}px"></div>{grid}{more}'
    return sec(t, m, body, bg=bg)

# ------------------------------------------------------------------ Tom
def tom(t, m, bg=None):
    k = t['k']
    ph = (f'<div style="width: {px(m,132,96)}px; height: {px(m,132,96)}px; flex: none; border-radius: {999 if k != "B" else 0}px; background: {t["ph"]}; display: flex; align-items: center; '
          f'justify-content: center; text-align: center; font-size: 12px; line-height: 1.3; color: {t["muted"]}; padding: 8px; box-sizing: border-box">[Photo: Tom Taggart]</div>')
    who = (f'<div><div style="font-family: {DISP}; font-weight: 600; font-size: {px(m,24,21)}px; color: {t["text"]}">Tom Taggart</div>'
           f'<div style="font-size: 16px; color: {t["muted"]}">Head of Business Development</div>'
           f'<div style="margin-top: 8px; font-size: 16px; color: {t["text"]}"><a href="tel:+17242720182" style="color: {t["text"]}; text-decoration: underline; text-underline-offset: 3px">(724) 272-0182</a> | <a href="mailto:tpt@sixpeakcapital.com" style="color: {t["text"]}; text-decoration: underline; text-underline-offset: 3px">tpt@sixpeakcapital.com</a></div></div>')
    btns = f'<div style="display: flex; flex-wrap: wrap; gap: 14px">{btn(t, m, "Book a call", full=m)}{btn(t, m, "Send a plan set", primary=False, full=m)}</div>'
    head = (f'{eyebrow(t, "Talk to us")}<div style="height: 14px"></div>{h2(t, m, "One call with Tom is the fastest way to a number.", 640)}'
            f'<div style="height: 14px"></div>{lead(t, m, "No presentation and no pitch deck. Tell him what you are building and where it stands.", 560)}')
    card = f'<div style="display: flex; gap: {px(m,24,16)}px; align-items: center">{ph}{who}</div><div style="height: 24px"></div>{btns}'
    if k == 'B':
        inner = (f'<div style="border-top: 2px solid {t["text"]}; padding-top: {px(m,40,28)}px; display: grid; grid-template-columns: repeat({px(m,2,1)}, minmax(0, 1fr)); gap: {px(m,64,28)}px; align-items: start">'
                 f'<div>{head}</div><div>{card}</div></div>')
    else:
        box = (f'background: {t["surface"]}; border-radius: 12px; padding: {px(m,48,24)}px; ' + ('' if k == 'A' else f'border: 1px solid {t["border"]}; '))
        inner = (f'<div style="{box}display: grid; grid-template-columns: repeat({px(m,2,1)}, minmax(0, 1fr)); gap: {px(m,64,28)}px; align-items: center">'
                 f'<div>{head}</div><div>{card}</div></div>')
    return sec(t, m, inner, bg=bg)

# ------------------------------------------------------------------ footer
DISCLAIMER = ('Rough order of magnitude estimates are prepared by LV Construction from plans on file with the City of Los Angeles. '
              'Unsolicited and for discussion only. Not a bid, proposal or offer to contract.')

def footer(t, m, disclaimer=False):
    k = t['k']
    lg = f'<div>{logo(t, m, panel=(k != "B"), h=34)}</div>'
    col = t['foottx']
    lines = (f'<div style="font-size: 14px; line-height: 1.7; color: {col}"><div style="font-weight: 600">LV Construction | A <a href="https://www.sixpeakcapital.com/" style="color: {col}; text-decoration: underline; text-underline-offset: 3px">Six Peak Capital</a> Company</div>'
             f'<div>CSLB Class B #1043604 and #1143510</div><div>560 Riverdale Dr, Glendale, CA 91204</div></div>')
    links = ''.join(f'<a href="#" style="display: inline-flex; align-items: center; min-height: 44px; font-size: 15px; color: {col}; text-decoration: underline; text-underline-offset: 4px">{l}</a>'
                    for l in ['How we price', 'ROM to GMP', 'Projects', 'Affordable housing', 'Team', 'Subcontractors', 'Contact us'])
    disc = (f'<div style="margin-top: 28px; padding-top: 20px; border-top: 1px solid {t["border"] if k != "C" else "rgba(191,199,218,0.18)"}; font-size: 13px; line-height: 1.6; color: {col}; max-width: 860px">{DISCLAIMER}</div>'
            if disclaimer else '')
    inner = (f'<div style="display: flex; flex-wrap: wrap; gap: {px(m,48,24)}px; justify-content: space-between; align-items: flex-start">'
             f'<div style="display: flex; flex-direction: column; gap: 18px">{lg}{lines}</div>'
             f'<nav aria-label="Footer" style="display: flex; flex-wrap: wrap; gap: {px(m,"4px 28px","0 22px")}; max-width: 520px">{links}</nav></div>{disc}')
    rule = f'border-top: 1px solid {t["border"]}; ' if k == 'B' else ''
    return f'<footer style="background: {t["foot"]}; {rule}padding: {px(m,56,40)}px 0">{wrap(m, inner)}</footer>'

# ------------------------------------------------------------------ home heroes
H1_HOME = 'We price your building from what ours actually cost.'
SUB_HOME = ('LV Construction is the building arm of Six Peak Capital. We learned these numbers as the owner paying the bills, '
            'and we estimate from subcontracts we have bought out on our own buildings.')

def h1(t, m, text, d=64, p=38, mw=860):
    return (f'<h1 style="margin: 0; font-family: {DISP}; font-weight: 600; font-size: {px(m,d,p)}px; line-height: 1.04; letter-spacing: -0.02em; text-wrap: balance; color: {t["text"]}; max-width: {mw}px">{text}</h1>')

def cta_home(t, m):
    return (f'<div style="display: flex; flex-wrap: wrap; gap: 14px">{btn(t, m, "How we price", full=m)}{btn(t, m, "Received a package from us?", primary=False, full=m)}</div>')

def hero_home(t, m):
    k = t['k']
    eb = eyebrow(t, 'General contractor | Los Angeles')
    if k == 'A':
        inner = (f'{eb}<div style="height: 20px"></div>{h1(t, m, H1_HOME)}<div style="height: 22px"></div>{lead(t, m, SUB_HOME, 640)}'
                 f'<div style="height: 32px"></div>{cta_home(t, m)}'
                 f'<div style="margin-top: {px(m,72,36)}px; font-size: 13px; color: {t["muted"]}">Berryman I, Mar Vista. Developed by Six Peak, built by LV.</div>')
        return (f'<section style="position: relative; background: {t["bg"]}; overflow: hidden">'
                f'<img src="{BLOB["berry"]}" alt="Berryman I at dusk" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; object-fit: cover">'
                f'<div style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; background: rgba(11,24,51,0.72)"></div>'
                f'<div style="position: relative; padding: {px(m,120,56)}px 0 {px(m,40,28)}px">{wrap(m, inner)}</div></section>')
    if k == 'B':
        top = (f'{eb}<div style="height: 22px"></div>{h1(t, m, H1_HOME, d=76, p=42, mw=1040)}<div style="height: {px(m,36,22)}px"></div>'
               f'<div style="display: grid; grid-template-columns: {px(m,"minmax(0, 1fr) auto","minmax(0, 1fr)")}; gap: {px(m,48,24)}px; align-items: end">'
               f'{lead(t, m, SUB_HOME, 520)}{cta_home(t, m)}</div>')
        photo = (f'<figure style="margin: {px(m,64,36)}px 0 0"><img src="{BLOB["berry"]}" alt="Berryman I at dusk" style="display: block; width: 100%; aspect-ratio: {px(m,"21 / 9","4 / 3")}; object-fit: cover">'
                 f'<figcaption style="margin-top: 12px; font-size: 14px; color: {t["muted"]}">Berryman I, Mar Vista. 156 leasable units. Developed by Six Peak, built by LV, delivered 2025.</figcaption></figure>')
        return sec(t, m, top + photo, pt=px(m, 88, 44), pb=0)
    left = (f'<div>{eb}<div style="height: 20px"></div>{h1(t, m, H1_HOME, d=56, p=36, mw=560)}<div style="height: 20px"></div>{lead(t, m, SUB_HOME, 520)}'
            f'<div style="height: 30px"></div>{cta_home(t, m)}</div>')
    card = (f'<div style="background: #FFFFFF; border: 1px solid {t["border"]}; border-radius: 12px; padding: {px(m,32,20)}px; box-shadow: 0 4px 20px rgba(0,0,0,0.08)">'
            f'{eyebrow(t, "When is the number real?")}<div style="height: {px(m,20,6)}px"></div>{stages(t, m, compact=True, h=130)}'
            f'<div style="margin-top: 22px; padding-top: 18px; border-top: 1px solid {t["border"]}; font-size: 15px; line-height: 1.5; color: {t["muted"]}">{ONE_LINE}</div></div>')
    grid = f'<div style="display: grid; grid-template-columns: {px(m,"minmax(0, 0.9fr) minmax(0, 1.1fr)","minmax(0, 1fr)")}; gap: {px(m,56,32)}px; align-items: center">{left}{card}</div>'
    return sec(t, m, grid, pt=px(m, 80, 40), pb=px(m, 56, 36))

# ------------------------------------------------------------------ package page pieces
H1_PKG = 'The number in your envelope, explained.'
SUB_PKG = ('We priced your building from the plans on file with the City. You did not ask for this, and it is not a bid. '
           'Here is how the number was built and how to get the full breakdown.')
CHIPS = ['We priced your plans', 'A cost sheet for your site', 'We could not price it', 'You already have a builder']

def selector(t, m):
    k = t['k']
    lab = f'<div style="font-size: 15px; font-weight: 600; color: {t["text"]}; margin-bottom: 12px">Which letter did you get?</div>'
    chips = ''
    for i, c in enumerate(CHIPS):
        on = i == 0
        if k == 'B':
            s = (f'background: transparent; border: none; border-bottom: 3px solid {RUST if on else "transparent"}; padding: 0 2px; min-height: 48px; '
                 f'font-family: {FONT}; font-size: 17px; font-weight: {700 if on else 500}; color: {t["text"] if on else t["muted"]}; border-radius: 0')
        else:
            if on:
                s = (f'background: {t["pillbg"]}; color: {t["pilltx"]}; border: 1.5px solid {t["pillbg"]}; padding: 0 18px; min-height: 48px; font-family: {FONT}; font-size: 16px; font-weight: 700; border-radius: 999px')
            else:
                s = (f'background: transparent; color: {t["text"]}; border: 1.5px solid {t["border"] if k == "A" else "rgba(11,24,51,0.28)"}; padding: 0 18px; min-height: 48px; font-family: {FONT}; font-size: 16px; font-weight: 500; border-radius: 999px')
        chips += f'<button type="button" aria-pressed="{"true" if on else "false"}" style="{s}">{c}</button>'
    gap = px(m, '8px 28px', '0 22px') if k == 'B' else '10px'
    br = f'border-bottom: 1px solid {t["border"]}; ' if k == 'B' else ''
    return f'<div>{lab}<div style="{br}display: flex; flex-wrap: wrap; gap: {gap}">{chips}</div></div>'

def cta_pkg(t, m):
    return (f'<div style="display: flex; flex-wrap: wrap; gap: 14px">{btn(t, m, "Get the full breakdown", full=m)}{btn(t, m, "Text Tom: (724) 272-0182", primary=False, full=m)}</div>')

def hero_pkg(t, m):
    k = t['k']
    eb = eyebrow(t, 'You received a package from LV')
    if k == 'A':
        inner = (f'{eb}<div style="height: 20px"></div>{h1(t, m, H1_PKG, d=60, p=36, mw=820)}<div style="height: 22px"></div>{lead(t, m, SUB_PKG, 660)}'
                 f'<div style="height: 32px"></div>{cta_pkg(t, m)}<div style="height: {px(m,56,36)}px"></div>{selector(t, m)}')
        return sec(t, m, inner, pt=px(m, 88, 44), pb=px(m, 72, 44))
    if k == 'B':
        inner = (f'<div style="max-width: 820px">{eb}<div style="height: 22px"></div>{h1(t, m, H1_PKG, d=68, p=40, mw=820)}<div style="height: 24px"></div>'
                 f'<p style="margin: 0; font-size: {px(m,21,18)}px; line-height: 1.55; color: {t["text"]}; max-width: 700px">We priced your building from the plans on file with the City. '
                 f'You did not ask for this, and it is <span style="font-weight: 700; color: {RUST}">not a bid</span>. Here is how the number was built and how to get the full breakdown.</p>'
                 f'<div style="height: 32px"></div>{cta_pkg(t, m)}</div><div style="height: {px(m,64,36)}px"></div>{selector(t, m)}')
        return sec(t, m, inner, pt=px(m, 88, 44), pb=px(m, 40, 24))
    left = (f'<div>{eb}<div style="height: 20px"></div>{h1(t, m, H1_PKG, d=52, p=36, mw=560)}<div style="height: 20px"></div>{lead(t, m, SUB_PKG, 520)}'
            f'<div style="height: 30px"></div>{cta_pkg(t, m)}</div>')
    card = (f'<div style="background: #FFFFFF; border: 1px solid {t["border"]}; border-radius: 12px; padding: {px(m,32,20)}px; box-shadow: 0 4px 20px rgba(0,0,0,0.08)">'
            f'{eyebrow(t, "Where your number sits")}<div style="height: {px(m,18,6)}px"></div>{stages(t, m, compact=True, marker=True, h=120)}'
            f'<div style="margin-top: 22px; padding-top: 18px; border-top: 1px solid {t["border"]}; font-size: 15px; line-height: 1.5; color: {t["muted"]}">{ONE_LINE}</div></div>')
    grid = f'<div style="display: grid; grid-template-columns: {px(m,"minmax(0, 0.9fr) minmax(0, 1.1fr)","minmax(0, 1fr)")}; gap: {px(m,56,32)}px; align-items: center">{left}{card}</div>'
    return sec(t, m, grid + f'<div style="height: {px(m,48,32)}px"></div>{selector(t, m)}', pt=px(m, 72, 40), pb=px(m, 72, 44))

IS = ['A budget you can underwrite with', 'Priced line by line across 16 trade divisions', 'Every assumption stated, with the plan sheet it came from']
ISNOT = ['Not a bid or an offer to contract', 'Not a guaranteed maximum price', 'Not held for any period']

def isnot(t, m, bg=None):
    k = t['k']
    def col(title, items, ic, colr):
        lis = ''.join(f'<li style="display: flex; gap: 14px; align-items: flex-start; padding: 14px 0; border-top: 1px solid {t["border"]}; font-size: {px(m,18,17)}px; line-height: 1.4; color: {t["text"]}">'
                      f'<span style="flex: none; margin-top: 1px">{icon(ic, colr, 24)}</span><span>{x}</span></li>' for x in items)
        box = ''
        if k == 'A':
            box = f'background: {t["surface"]}; border-radius: 12px; padding: {px(m,32,22)}px; '
        elif k == 'C':
            box = f'background: #FFFFFF; border: 1px solid {t["border"]}; border-radius: 12px; padding: {px(m,32,22)}px; '
        return (f'<div style="{box}"><h3 style="margin: 0 0 16px; font-family: {DISP}; font-weight: 600; font-size: {px(m,28,24)}px; color: {t["text"]}">{title}</h3>'
                f'<ul style="list-style: none; margin: 0; padding: 0">{lis}</ul></div>')
    pos = {'A': '#BFC7DA', 'B': '#4E7A3A', 'C': '#4E7A3A'}[k]
    neg = {'A': '#E8935A', 'B': '#A84A15', 'C': '#A84A15'}[k]
    body = (f'{eyebrow(t, "Read it the right way")}<div style="height: 14px"></div>{h2(t, m, "What a ROM is, and what it is not")}<div style="height: {px(m,40,24)}px"></div>'
            f'<div style="display: grid; grid-template-columns: repeat({px(m,2,1)}, minmax(0, 1fr)); gap: {px(m,32,18)}px">'
            f'{col("What it is", IS, IC_CHECK, pos)}{col("What it is not", ISNOT, IC_X, neg)}</div>')
    return sec(t, m, body, bg=bg)

NEXT = [('Answer the one question in the letter.', 'A line back to Tom, or a text, is all it takes.'),
        ('We re-run the number.', 'You get the full 16-division breakdown the same week.'),
        ('Tom calls on Thursday.', 'If a builder is already on this one, keep our number as a check on theirs, and tell us about the next project.')]

def nextsteps(t, m, bg=None):
    k = t['k']
    cells = ''
    for i, (a, b) in enumerate(NEXT):
        cells += (f'<li style="display: flex; gap: {px(m,24,16)}px; align-items: flex-start; padding: {px(m,26,20)}px 0; border-top: 1px solid {t["border"]}">'
                  f'<span style="flex: none; width: {px(m,64,44)}px; font-family: {DISP}; font-weight: 700; font-size: {px(m,48,36)}px; line-height: 1; color: {t["accent"]}">{i+1}</span>'
                  f'<span><span style="display: block; font-family: {DISP}; font-weight: 600; font-size: {px(m,24,20)}px; color: {t["text"]}">{a}</span>'
                  f'<span style="display: block; margin-top: 6px; font-size: {px(m,18,16)}px; line-height: 1.5; color: {t["muted"]}">{b}</span></span></li>')
    body = (f'{eyebrow(t, "What happens next")}<div style="height: 14px"></div>{h2(t, m, "Three steps to the full breakdown")}<div style="height: {px(m,32,20)}px"></div>'
            f'<ol style="list-style: none; margin: 0; padding: 0; max-width: 860px">{cells}</ol><div style="height: {px(m,28,20)}px"></div>{cta_pkg(t, m)}')
    return sec(t, m, body, bg=bg)

# ------------------------------------------------------------------ page assembly
NOTE_PKG = 'Priced from 451 bought-out trade lines across 33 trades, on 15 LV projects. Library as of 19 October 2026.'

def page_home(t, m):
    k = t['k']
    if k == 'A':
        parts = [nav(t, m), hero_home(t, m), counters(t, m), doors(t, m), explainer(t, m, bg=t['bg2']), projects(t, m), tom(t, m, bg=t['bg2']), footer(t, m)]
    elif k == 'B':
        parts = [nav(t, m), hero_home(t, m), counters(t, m), explainer(t, m), projects(t, m, bg=t['bg2']), doors(t, m), tom(t, m, bg=None), footer(t, m)]
    else:
        parts = [nav(t, m), hero_home(t, m), counters(t, m), steps(t, m, bg=t['bg2']), doors(t, m), projects(t, m, bg=t['bg2']), tom(t, m), footer(t, m)]
    return ''.join(parts)

def page_pkg(t, m):
    k = t['k']
    st = steps(t, m, title='How your number was built', note=NOTE_PKG, eb='Behind the number', bg=(t['bg2'] if k != 'B' else None))
    pj = projects(t, m, n=3, title='Three LV buildings closest to yours', eb='Who we are', intro=False, stats=False, bg=(t['bg2'] if k != 'B' else None))
    if k == 'C':
        parts = [nav(t, m, True), hero_pkg(t, m), st, isnot(t, m), nextsteps(t, m, bg=t['bg2']), pj, tom(t, m), footer(t, m, True)]
    elif k == 'A':
        parts = [nav(t, m, True), hero_pkg(t, m), st, isnot(t, m), explainer(t, m, compact=True, marker=True, bg=t['bg2'], title='When your number becomes a guarantee'),
                 nextsteps(t, m), pj, tom(t, m), footer(t, m, True)]
    else:
        parts = [nav(t, m, True), hero_pkg(t, m), st, isnot(t, m, bg=t['bg2']), explainer(t, m, compact=True, marker=True, title='When your number becomes a guarantee'),
                 nextsteps(t, m, bg=t['bg2']), pj, tom(t, m), footer(t, m, True)]
    return ''.join(parts)

def doc(t, title, body, w, h, css=''):
    props = json.dumps({"$preview": {"width": w, "height": h}})
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>{title}</title>
<script src="./support.js"></script>
</head>
<body>
<x-dc>
<helmet>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&amp;family=DM+Sans:wght@500;600;700&amp;display=swap">
<style>
body{{margin:0}}
a{{color:{t["link"]}}}a:hover{{color:{t["linkh"]}}}
{css}</style>
</helmet>
<div style="width: 100%; box-sizing: border-box; background: {t["bg"]}; color: {t["text"]}; font-family: {FONT}; font-size: 17px; line-height: 1.5">{body}</div>
</x-dc>
<script type="text/x-dc" data-dc-script data-props='{props}'>
class Component extends DCLogic {{
renderVals() {{
return {{}};
}}
}}
</script>
</body>
</html>
'''

BOARDS = []  # (file, title, dir, page, mobile)
for k in 'ABC':
    for pg in ('Home', 'Package'):
        for dev in ('Desktop', 'Phone'):
            f = 'Main.dc.html' if (k, pg, dev) == ('A', 'Home', 'Desktop') else f'{k}_{pg}_{dev}.dc.html'
            BOARDS.append((f, f'{k} {T[k]["name"]}: {"Homepage" if pg == "Home" else "Package landing page"}, {dev.lower()}', k, pg, dev == 'Phone'))

def build(heights):
    os.makedirs(OUT, exist_ok=True)
    for f, title, k, pg, m in BOARDS:
        t = T[k]
        body = page_home(t, m) if pg == 'Home' else page_pkg(t, m)
        w = 390 if m else 1440
        open(os.path.join(OUT, f), 'w', encoding='utf-8').write(doc(t, title, body, w, heights.get(f, 3000)))

def canvas(heights):
    boards, order = {}, []
    colx = {'A': 0, 'B': 2150, 'C': 4300}
    home_h = max(heights[f] for f, _, k, pg, m in BOARDS if pg == 'Home')
    row2 = home_h + 420
    for f, title, k, pg, m in BOARDS:
        x = colx[k] + (1520 if m else 0)
        y = 0 if pg == 'Home' else row2
        boards[f] = {"x": x, "y": y, "w": 390 if m else 1440, "h": heights[f], "title": title, "expand": "fill"}
        order.append(f)
    notes = {}
    for k in 'ABC':
        notes[f'title{k}'] = {"x": colx[k], "y": -300, "text": f'{k}. {T[k]["name"]}', "kind": "title1", "maxW": 1910}
        notes[f'pkg{k}'] = {"x": colx[k], "y": row2 - 300, "text": f'{k}. Package landing page', "kind": "title1", "maxW": 1910}
    idx = {"v": 3, "createdOnFiles": {"v": 1, "at": "2026-11-19T00:20:00Z"}, "title": "LV website mockups: round 1 (three directions)",
           "launch": {"view": "canvas"}, "pages": [], "boards": boards, "order": order, "notes": notes, "designSystems": []}
    json.dump(idx, open(os.path.join(OUT, 'canvas.json'), 'w', encoding='utf-8'), indent=1)

if __name__ == '__main__':
    hp = '/home/claude/lvmock/heights.json'
    heights = json.load(open(hp)) if os.path.exists(hp) else {}
    build(heights)
    if heights:
        canvas(heights)
    print('built', len(BOARDS), 'boards; heights known:', bool(heights))
