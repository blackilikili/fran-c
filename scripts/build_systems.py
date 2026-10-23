"""Build the systems portfolio into docs/systems/.

Each page body lives in src/systems/pages/<slug>.html. This script wraps it in the shared
layout (head metadata, header, footer), copies the assets and writes docs/systems/<slug>.html.
Run: python3 scripts/build_systems.py
"""
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "src" / "systems"
OUT = ROOT / "docs" / "systems" / "systems"
SITE = "https://fran-c-portfolio.netlify.app"
BASE = SITE + "/systems/systems/"
EMAIL = "fran.f.crystal@gmail.com"

# slug: (nav label or None, <title>, meta description)
PAGES = {
    "index": ("Home", "Fran C. · Funnel, CRM & Marketing Automation Specialist",
              "Funnel builder and CRM integration specialist. Fran C. connects landing pages, assessments, CRM records, "
              "email automation and booking workflows into one working customer journey."),
    "services": ("Services", "Services · Funnels, CRM, Email Automation & Marketing Ops · Fran C.",
                 "Funnel architecture, CRM setup and integration, email marketing automation and marketing operations "
                 "support for coaches, consultants, course creators and agencies."),
    "blueprints": ("Blueprints", "Funnel Blueprints · Assessment, VSL, Webinar & Enrollment Funnels · Fran C.",
                   "Six funnel architectures mapped step by step: assessment funnels, VSL booking funnels, masterclass "
                   "and webinar funnels, lead magnets, applications and course enrollment."),
    "projects": ("Projects", "Projects · Fran C.",
                 "Assessment experiences, profile-based offers and sales funnels Fran C. has worked on, with each "
                 "claim marked as verified, to be confirmed or representative."),
    "tools": ("Tools", "Tools & Platforms · GoHighLevel, HubSpot, Kajabi, Kit, Kartra · Fran C.",
              "The CRM, funnel, email and website platforms Fran C. works with, organised by the part of the customer "
              "journey they support."),
    "about": ("About", "About · Fran C., Marketing Operations Specialist",
              "15 years of professional experience, remote since 2016. Fran C. combines marketing implementation "
              "with operational thinking."),
    "contact": (None, "Contact · Discuss Your Funnel or CRM Project · Fran C.",
                "Get in touch about a funnel build, CRM integration, marketing automation or ongoing implementation support."),
    "thanks": (None, "Message sent · Fran C.", "Thank you for getting in touch."),
}

FONTS = ("https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,400;12..96,600;12..96,800"
         "&family=Instrument+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500;600&display=swap")


def nav(current):
    links = []
    for slug, (label, _, _) in PAGES.items():
        if not label:
            continue
        href = "index.html" if slug == "index" else f"{slug}.html"
        cur = ' aria-current="page"' if slug == current else ""
        links.append(f'<a href="{href}"{cur}>{label}</a>')
    cta_cur = ' aria-current="page"' if current == "contact" else ""
    links.append(f'<a class="nav-cta" href="contact.html"{cta_cur}>Let\'s talk</a>')
    return "\n      ".join(links)


def layout(slug, body):
    _, title, desc = PAGES[slug]
    url = BASE if slug == "index" else f"{BASE}{slug}.html"
    # Only the home page is reached at a folder URL, so only it needs a base for relative links.
    base = '<base href="/systems/systems/">\n' if slug == "index" else ""
    robots = '<meta name="robots" content="noindex">\n' if slug == "thanks" else ""
    return f"""<!doctype html>
<html lang="en" class="no-js">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
{base}<link rel="icon" href="/favicon-32.png" sizes="32x32" type="image/png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="shortcut icon" href="/favicon.ico">
<title>{title}</title>
<meta name="description" content="{desc}">
{robots}<link rel="canonical" href="{url}">
<meta property="og:type" content="website">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{BASE}og.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Fran C. Funnels, CRM and automations that work together.">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="{BASE}og.jpg">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="{FONTS}">
<link rel="stylesheet" href="assets/systems.css">
<script src="assets/systems.js" defer></script>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="site-head">
  <div class="wrap">
    <a class="logo" href="index.html">Fran C<i>.</i> <small>Systems</small></a>
    <button class="menu-btn" type="button" aria-expanded="false" aria-controls="site-nav">Menu</button>
    <nav id="site-nav" class="nav" aria-label="Main">
      {nav(slug)}
    </nav>
  </div>
</header>
<main id="main">
{body.strip()}
</main>
<footer class="site-foot">
  <div class="wrap">
    <div class="foot-top">
      <div>
        <a class="logo" href="index.html">Fran C<i>.</i></a>
        <p style="margin-top:8px;max-width:46ch">Funnels, CRM records, email automation and booking workflows, connected into one customer journey.</p>
      </div>
      <nav class="foot-nav" aria-label="Footer">
        <a href="services.html">Services</a><a href="blueprints.html">Blueprints</a><a href="projects.html">Projects</a>
        <a href="tools.html">Tools</a><a href="about.html">About</a><a href="contact.html">Contact</a>
      </nav>
    </div>
    <div class="foot-bottom">
      <span>{EMAIL} · Remote, based in the Philippines</span>
      <span>Also see my <a href="../socialmedia/">social media &amp; content portfolio</a></span>
    </div>
  </div>
</footer>
</body>
</html>
"""


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    shutil.copytree(SRC / "assets", OUT / "assets", dirs_exist_ok=True)
    og = SRC / "og.jpg"
    if og.exists():
        shutil.copy(og, OUT / "og.jpg")
    # Site-wide files (favicons, Netlify redirects) live at the deploy root.
    for f in (ROOT / "src" / "root").iterdir():
        shutil.copy(f, ROOT / "docs" / f.name)
    for slug in PAGES:
        body = (SRC / "pages" / f"{slug}.html").read_text()
        (OUT / f"{slug}.html").write_text(layout(slug, body))
    print(f"built {len(PAGES)} pages into {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
