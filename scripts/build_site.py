"""Build the public site in docs/ from drafts/v3-split.html.

Strips artifact-only markup, adds a full HTML head with link-preview tags,
renames images to neutral filenames and resizes them for the web.
"""
import re, shutil
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "drafts" / "v3-split.html"
OUT = ROOT / "docs"
SITE = "https://fran-c-sm-portfolio.netlify.app"

RENAME = {
    "hh-carousel-know-now": "personal-brand-01", "hh-carousel-islam-ei": "personal-brand-02",
    "hh-reel-next-move": "personal-brand-03", "hh-fb-cacao-offer": "personal-brand-04",
    "hh-fb-not-about-money": "personal-brand-05",
    "hearty-internal-compass": "leadership-01", "hearty-team-problem": "leadership-02",
    "hearty-g17-guest-speaker": "leadership-03",
    "sourcingxpro-landed-cost": "b2b-01", "sourcingxpro-biotech-merch": "b2b-02", "sourcingxpro-risk-video": "b2b-03",
    "drsamwhite-testimonial": "health-01", "drsamwhite-essential-fatty-acids": "health-02", "drsamwhite-leaky-gut": "health-03",
    "lighthouse-quote-doctor-uk": "advocacy-01", "lighthouse-quote-doctor": "advocacy-02", "lighthouse-quote-educator": "advocacy-03",
    "starrz-awake-masterclass": "events-01", "starrz-wellness-expo": "events-02", "starrz-podcast-ep181": "events-03",
}

TITLE = "Fran C. · Social Media &amp; Content"
DESC = ("Fran C.: social-first content, carried all the way to published. A content creator with an operations "
        "background: 15 years of making sure good work actually ships.")

s = SRC.read_text()
body = s.split("</title>", 1)[1].replace('<meta name="claude:viewport-fit-sides" content="cover">\n', "")
body = re.sub(r'<div class="ver">.*?</div></div>\n\n', "", body, flags=re.S)
links, rest = body[: body.index("<style>")], body[body.index("<style>"):]
style, content = rest[: rest.index("</style>") + 8], rest[rest.index("</style>") + 8:]

used = sorted(set(re.findall(r"img/([\w-]+)\.jpg", content)))
for old in used:
    content = content.replace(f"img/{old}.jpg", f"img/{RENAME[old]}.jpg")

# Link to the systems portfolio (public site only; the Claude preview has no systems/ folder).
content = content.replace(
    '<nav><a href="#work">Work</a><a href="#behind">Behind it</a><a href="#contact">Contact</a></nav>',
    '<nav><a href="#work">Work</a><a href="#behind">Behind it</a><a href="systems/">Funnels &amp; CRM</a><a href="#contact">Contact</a></nav>', 1)
content = content.replace(
    "<p class=\"sub\">Where content goes after it's posted: the wider marketing systems Fran has worked in.</p>",
    "<p class=\"sub\">Where content goes after it's posted: the wider marketing systems Fran has worked in. "
    "<a href=\"systems/\" style=\"color:#fff;font-weight:600\">See the funnel &amp; CRM portfolio →</a></p>", 1)
assert 'href="systems/"' in content, "systems link not inserted"

head = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{TITLE}</title>
<meta name="description" content="{DESC}">
<meta property="og:title" content="{TITLE}">
<meta property="og:description" content="{DESC}">
<meta property="og:type" content="website">
<meta property="og:url" content="{SITE}/">
<meta property="og:image" content="{SITE}/og.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Fran C. Social-first content, carried all the way to published. Social Media Manager, Content Editor, Content Marketing.">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="{SITE}/og.jpg">
{links.strip()}
{style}
</head>
<body>
{content.strip()}
</body>
</html>
"""

# Only replace this site's own files; docs/systems/ (the systems portfolio) is built separately.
shutil.rmtree(OUT / "img", ignore_errors=True)
(OUT / "img").mkdir(parents=True)
(OUT / ".nojekyll").touch()
(OUT / "index.html").write_text(head)
for old in used:
    im = Image.open(ROOT / "drafts" / "img" / f"{old}.jpg")
    if im.width > 1400:
        im = im.resize((1400, round(im.height * 1400 / im.width)))
    im.save(OUT / "img" / f"{RENAME[old]}.jpg", quality=84, optimize=True)
print(f"built docs/ with {len(used)} images")
