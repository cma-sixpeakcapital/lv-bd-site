# LV Construction website: redesign draft

Branch `redesign`. The live site (lvllc.com) is published from `main` and is not changed by this branch.

## What this is

The pages approved as mockups on 18 and 19 November 2026 ("Light editorial", banner option B), built as a real site:

| Page | Address |
|---|---|
| Homepage | `/` |
| Package landing page | `/package` |
| How we price | `/how-we-price` |
| ROM to GMP | `/rom-to-gmp` |
| Projects | `/projects` |
| Project pages, one per completed building | `/projects/berryman-1`, `/projects/berryman-2`, `/projects/reading`, `/projects/wilton`, `/projects/venice`, `/projects/oxford`, `/projects/kenmore`, `/projects/bonner` |
| Affordable housing | `/affordable-housing` |
| Team | `/team` |
| Contact us | `/contact` |
| Subcontractors | `/subcontractors` |

## How it is put together

- `tools/sitegen/gen.py` and `gen2.py` hold the page content and layout (the same generator that drew the mockups).
- `tools/sitegen/build_site.py` writes `site/*.html` and `static/site/site.css`. Run it after any change: `python3 tools/sitegen/build_site.py`.
- `app.py` serves the built pages. Run locally with `python3 app.py`, then open http://localhost:5002.
- The eight project pages come from one template and the `BUILT` table in `gen2.py` (address, structure, architect, photos). Add a building there and rebuild.
- Photos used by the pages are in `static/site/img/` (project page photos in `static/site/img/projects/`). Team headshots are stored there too, not loaded from Squarespace.
- `static/images/` and `templates/` are the current live site's files, kept untouched for reference and for the project photo library.

Each page carries two layouts: desktop from 900px wide, phone below. Between 900px and 1199px the desktop layout is scaled to fit.

## Draft status

- Any address other than lvllc.com is kept out of search engines (`X-Robots-Tag: noindex` and a disallow-all `robots.txt`).
- The contact form posts to `/api/contact` in `app.py`. It sends nothing until the settings under "Contact form" below are filled in; until then a visitor who presses Send is told to reach Tom directly.
- Moving parts (counting figures, the seven-step graphic on the homepage, the ROM to GMP explainer player, the project map and its filter tabs) are in `tools/sitegen/site.js` and `tools/sitegen/extra.css`. The map uses Leaflet (in `static/site/vendor/`) with OpenStreetMap tiles; pin positions are in `GEO` in `gen2.py`.
- The one-page ROM to GMP PDF linked from `/rom-to-gmp` is a draft that has not been approved.
- Text in [square brackets] is content still to come.
- The address of the package landing page (`/package`) is a working name. Settle it before it is printed in any letter.

## Before this replaces the live site

- Fill in the contact form settings (below) and send a test note.
- Replace every [bracketed] placeholder.
- Choose a map tile provider for production traffic (the draft uses the public OpenStreetMap tiles).
- Confirm the seven-step wording on the homepage. (The 70% figure on `/subcontractors` was verified with Grady on 19 November 2026.)
- Decide the hosting plan (the live service is on Render's free plan, which sleeps when idle).
- Merge into `main` only after Chris approves.

## Contact form

Each note from `/contact` is emailed to Tom with Chris copied. Replying to the email answers the person who wrote.

Email is sent through Resend (resend.com) over HTTPS, because Render's free plan blocks the ordinary mail ports. Set these in the Render service under Environment. No address or key is stored in this repository.

| Setting | Value |
|---|---|
| `RESEND_API_KEY` | The sending key from the Resend account |
| `CONTACT_TO` | Tom's address |
| `CONTACT_CC` | Chris's address (several addresses are separated by commas) |
| `CONTACT_FROM` | Optional. The sender shown, on a domain verified with Resend. Default: `LV Construction website <website@lvllc.com>` |

Notes sent from any address other than lvllc.com carry "[Draft site test]" in the subject. Junk is filtered by a hidden field, a two-second minimum and a limit of five notes an hour from one connection.
