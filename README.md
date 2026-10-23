# Fran C. · Portfolio sites

Two linked static sites, deployed together from `docs/`:

| Site | Public path | Source |
|---|---|---|
| Social media & content portfolio | `/systems/socialmedia/` | `drafts/v3-split.html` → `scripts/build_site.py` |
| Funnel, CRM & marketing automation portfolio | `/systems/systems/` | `src/systems/` → `scripts/build_systems.py` |

Plain HTML, CSS and a little JavaScript. No framework, no database, no API keys.

## Build

Requires Python 3 and Pillow (`pip install pillow`).

```bash
python3 src/systems/data/make_blueprints.py   # only after editing funnel data
python3 src/systems/data/make_projects.py     # only after editing project data
python3 scripts/build_site.py                 # social site -> docs/systems/socialmedia/
python3 scripts/build_systems.py              # systems site -> docs/systems/systems/, plus favicons and _redirects at docs/
```

Preview locally: `cd docs && python3 -m http.server 8000`, then open http://localhost:8000/systems/socialmedia/ and http://localhost:8000/systems/systems/.

## Deploy (Netlify)

Drag the `docs` folder (or a zip of its contents, unzipped) onto the site's **Deploys** page in Netlify. `index.html` must be at the top level of what you upload.

Link previews use absolute URLs on `https://fran-c-portfolio.netlify.app`. If the domain changes, update `SITE` in both build scripts.

## Contact form

`/systems/systems/contact.html` uses **Netlify Forms** (`data-netlify="true"`). Netlify detects it automatically on deploy. To receive submissions by email: Netlify → Site → Forms → enable form detection if prompted, then add an email notification for `project-inquiry`. The form only works on Netlify; on any other host, visitors are told to email directly.

## Updating project case studies

Edit `PROJECTS` in `src/systems/data/make_projects.py`. Any field left as `None` shows "To be confirmed". Fill in only details Fran has confirmed, then re-run the generator and build.

## Content rules

See `FACTS.md`: no invented results, metrics, testimonials or responsibilities; no dates on the social site; clients described, not named, on the social site.

## Redirects and icons

`src/root/` holds files copied to the deploy root: `_redirects` (`/` goes to the social portfolio, `/systems/` to the systems portfolio) and the FC favicons.
