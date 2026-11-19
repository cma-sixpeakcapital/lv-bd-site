# LV Construction website: redesign draft

Branch `redesign`. The live site (lvllc.com) is published from `main` and is not changed by this branch.

## What this is

The nine pages approved as mockups on 18 and 19 November 2026 ("Light editorial", banner option B), built as a real site:

| Page | Address |
|---|---|
| Homepage | `/` |
| Package landing page | `/package` |
| How we price | `/how-we-price` |
| ROM to GMP | `/rom-to-gmp` |
| Projects | `/projects` |
| Project page (Reading) | `/projects/reading` |
| Affordable housing | `/affordable-housing` |
| Team | `/team` |
| Contact us | `/contact` |
| Subcontractors | `/subcontractors` |

## How it is put together

- `tools/sitegen/gen.py` and `gen2.py` hold the page content and layout (the same generator that drew the mockups).
- `tools/sitegen/build_site.py` writes `site/*.html` and `static/site/site.css`. Run it after any change: `python3 tools/sitegen/build_site.py`.
- `app.py` serves the built pages. Run locally with `python3 app.py`, then open http://localhost:5002.
- Photos used by the pages are in `static/site/img/`. Team headshots are stored there too, not loaded from Squarespace.
- `static/images/` and `templates/` are the current live site's files, kept untouched for reference and for the project photo library.

Each page carries two layouts: desktop from 900px wide, phone below. Between 900px and 1199px the desktop layout is scaled to fit.

## Draft status

- Any address other than lvllc.com is kept out of search engines (`X-Robots-Tag: noindex` and a disallow-all `robots.txt`).
- Not connected yet: the contact form (sends nothing).
- Moving parts (counting figures, the seven-step graphic on the homepage, the ROM to GMP explainer player, the project map and its filter tabs) are in `tools/sitegen/site.js` and `tools/sitegen/extra.css`. The map uses Leaflet (in `static/site/vendor/`) with OpenStreetMap tiles; pin positions are in `GEO` in `gen2.py`.
- The one-page ROM to GMP PDF linked from `/rom-to-gmp` is a draft that has not been approved.
- Text in [square brackets] is content still to come.
- The address of the package landing page (`/package`) is a working name. Settle it before it is printed in any letter.

## Before this replaces the live site

- Connect the contact form.
- Replace every [bracketed] placeholder.
- Choose a map tile provider for production traffic (the draft uses the public OpenStreetMap tiles).
- Confirm the 70% figure on `/subcontractors` and the seven-step wording on the homepage.
- Decide the hosting plan (the live service is on Render's free plan, which sleeps when idle).
- Merge into `main` only after Chris approves.
