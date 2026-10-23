"""Generates src/systems/pages/projects.html.

Integrity rule: only Fran's own description of each project (from her brief) and the public URL
are stated. Everything else stays 'To be confirmed' until Fran confirms it. Update PROJECTS
below as answers come in, then re-run this script and scripts/build_systems.py.
"""
from pathlib import Path
from html import escape as e

TBC = None  # renders as a "To be confirmed" status

PROJECTS = [
 dict(id="courage-type", name="Courage Type", url="https://couragetype.com", kind="Brand & offer website",
      brief="A brand website where the presentation, messaging and visual hierarchy carry the offer.",
      blueprint=None),
 dict(id="four-worlds", name="The Four Worlds", url="https://thefourworlds.com/", kind="Framework experience",
      brief="A brand built around a framework, guiding visitors through a specific concept or experience.",
      blueprint=None),
 dict(id="zipline", name="Zipline Consulting Assessment", url="https://assessment.ziplineconsulting.com/", kind="Assessment",
      brief="An assessment experience: question flow, lead capture and the link between the answers and the insights a person receives.",
      blueprint=("assessment", "Assessment → results → CRM → email")),
 dict(id="eli", name="Riana Malia: ELI", url="https://riana-malia-eli.vercel.app/eli", kind="Diagnostic assessment",
      brief="A diagnostic assessment experience with its own interface, hosted as a web app.",
      blueprint=("assessment", "Assessment → results → CRM → email")),
 dict(id="powerhouse", name="Powerhouse Profile", url="https://www.powerhouseprofile.com/", kind="Profile-based offer",
      brief="A profile-based, assessment-led offer, with a value proposition and customer journey built around the profile.",
      blueprint=("assessment", "Assessment → results → CRM → email")),
 dict(id="salesclosers", name="SalesClosers", url="https://salesclosers.com/", kind="Service & sales funnel",
      brief="A service business whose site positions the offer and moves visitors toward a sales conversation.",
      blueprint=("vsl", "Landing page → VSL → booked call")),
]

FIELDS = [
 ("My role", "role", "Built, supported or maintained: which parts were mine."),
 ("Pages and experiences", "pages", "The funnels, forms or pages I worked on."),
 ("CRM, email &amp; integrations", "systems", "The components I configured or maintained."),
 ("Problem addressed", "problem", "What wasn't working, or what needed building."),
 ("Deliverable", "deliverable", "What was handed over or improved."),
 ("Tools used", "tools", "Platforms used on this project."),
]

def status(v):
    return '<span class="status pending">To be confirmed</span>' if v is None else '<span class="status verified">Confirmed</span>'

def card(p):
    return f"""
      <button class="proj" type="button" data-open="{p['id']}" aria-haspopup="dialog">
        <span class="proj-top"><span class="kind">{e(p['kind'])}</span><b>{e(p['name'])}</b></span>
        <span class="proj-bottom">
          <span class="chips"><span class="status pending">Details to be confirmed</span></span>
          <p>{e(p['brief'])}</p>
          <span class="open">Open case study</span>
        </span>
      </button>"""

def dialog(p):
    rows = "".join(f"""
          <div class="box"><div class="field-row"><h3>{label}</h3>{status(p.get(key))}</div>
            <p class="muted">{e(p[key]) if p.get(key) else hint}</p></div>""" for label, key, hint in FIELDS)
    if p["blueprint"]:
        bp = f"""<div class="box note"><div class="field-row"><h3>Workflow</h3><span class="status blueprint">Representative blueprint</span></div>
            <p>Until the specifics are confirmed, this is the closest representative workflow. It shows how this kind of journey is typically built. It is not a diagram of this client's account.</p>
            <a class="link-arrow" href="blueprints.html#{p['blueprint'][0]}">{e(p['blueprint'][1])}</a></div>"""
    else:
        bp = """<div class="box note"><div class="field-row"><h3>Workflow</h3><span class="status pending">To be confirmed</span></div>
            <p>The workflow diagram will be added once the scope of the work is confirmed.</p></div>"""
    return f"""
<dialog class="case" id="{p['id']}" aria-labelledby="{p['id']}-title">
  <div class="case-top">
    <button class="case-close" type="button" data-close>Close</button>
    <span class="eyebrow" style="color:#FF9C7E">{e(p['kind'])}</span>
    <h2 id="{p['id']}-title">{e(p['name'])}</h2>
    <p style="color:#C9D5E3;max-width:60ch">{e(p['brief'])}</p>
    <a href="{p['url']}" target="_blank" rel="noopener">Visit the live site ↗</a>
  </div>
  <div class="case-body">
    <div class="case-grid">{rows}
    </div>
    {bp}
    <div class="box"><div class="field-row"><h3>Screenshots</h3><span class="status pending">To be added</span></div>
      <p class="muted">Annotated page views will be added with the client's permission.</p></div>
  </div>
</dialog>"""

html = f"""<section class="page-hero">
  <div class="wrap">
    <span class="eyebrow">Projects</span>
    <h1>Assessments, profile offers and <span class="accent">sales journeys.</span></h1>
    <p class="lede">Each project below is marked honestly. Live sites only show the front end, so I don't describe the systems behind them until the details of my role are confirmed.</p>
  </div>
</section>

<section class="section" style="padding-top:8px">
  <div class="wrap">
    <div class="integrity" aria-label="How to read these case studies">
      <div><span class="status verified">Confirmed</span><span>Work I personally implemented, supported or maintained, confirmed for this portfolio.</span></div>
      <div><span class="status pending">To be confirmed</span><span>Details still being confirmed. Nothing is claimed until it is.</span></div>
      <div><span class="status blueprint">Representative blueprint</span><span>How this kind of journey is typically built. Not a diagram of a client's account.</span></div>
    </div>
    <div class="proj-grid">{"".join(card(p) for p in PROJECTS)}
    </div>
    <div class="cta-band" style="margin-top:56px">
      <div><h2>Have an assessment or funnel that needs connecting?</h2><p>I'm happy to look at what you have and explain how I'd approach it.</p></div>
      <a class="btn" href="contact.html">Discuss your project</a>
    </div>
  </div>
</section>
{"".join(dialog(p) for p in PROJECTS)}
"""
out = Path(__file__).resolve().parent.parent / "pages" / "projects.html"
out.write_text(html)
print("wrote", out)
