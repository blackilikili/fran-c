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

# One-page site: slug -> (unused, <title>, meta description)
PAGES = {
    "index": ("Home", "Fran C. · Funnel Builder, CRM & Marketing Automation Specialist",
              "Funnel builder and CRM integration specialist. Fran C. builds assessment, masterclass, book-a-call, "
              "application and lead gathering funnels, connected to CRM records and email automation."),
}

SECTIONS = [("builds", "Builds"), ("funnels", "Funnels"), ("services", "Services"), ("tools", "Tools"), ("about", "About")]

FONTS = ("https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,400;12..96,600;12..96,800"
         "&family=Instrument+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500;600&display=swap")


def nav(current):
    links = [f'<a href="#{sid}">{label}</a>' for sid, label in SECTIONS]
    links.append('<a class="nav-cta" href="#contact">Let\'s talk</a>')
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
<body id="top">
<a class="skip" href="#main">Skip to content</a>
<header class="site-head">
  <div class="wrap">
    <a class="logo" href="#top">Fran C<i>.</i> <small>Systems</small></a>
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
        <a class="logo" href="#top">Fran C<i>.</i></a>
        <p style="margin-top:8px;max-width:46ch">Funnels, CRM records, email automation and booking workflows, connected into one customer journey.</p>
      </div>
      <nav class="foot-nav" aria-label="Footer">
        <a href="#builds">Builds</a><a href="#funnels">Funnels</a><a href="#services">Services</a>
        <a href="#tools">Tools</a><a href="#about">About</a><a href="#contact">Contact</a>
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
    shutil.rmtree(OUT, ignore_errors=True)
    OUT.mkdir(parents=True, exist_ok=True)
    shutil.copytree(SRC / "assets", OUT / "assets", dirs_exist_ok=True)
    shutil.copytree(SRC / "img", OUT / "img", dirs_exist_ok=True)
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
