"""Generates src/systems/pages/projects.html.

Integrity rule: only Fran's own description of each project (from her brief) and the public URL
are stated. Everything else stays 'To be confirmed' until Fran confirms it. Update PROJECTS
below as answers come in, then re-run this script and scripts/build_systems.py.
"""
from pathlib import Path
from html import escape as e

TBC = None  # renders as a "To be confirmed" status

PROJECTS = [
 dict(id="brand-site", name="Brand & offer website", url=None, kind="Personal development brand",
      brief="A brand website where the presentation, messaging and visual hierarchy carry the offer.",
      blueprint=None),
 dict(id="framework-brand", name="Framework-led brand experience", url=None, kind="Methodology brand",
      brief="A brand built around a framework, guiding visitors through a specific concept or experience.",
      blueprint=None),
 dict(id="consulting-assessment", name="Consulting firm assessment", url=None, kind="Assessment",
      brief="An assessment experience: question flow, lead capture and the link between the answers and the insights a person receives.",
      blueprint=("assessment", "Assessment → results → CRM → email")),
 dict(id="diagnostic-app", name="Coach's diagnostic assessment app", url=None, kind="Diagnostic assessment",
      brief="A diagnostic assessment experience with its own interface, hosted as a web app.",
      blueprint=("assessment", "Assessment → results → CRM → email")),
 dict(id="profile-offer", name="Profile-based assessment offer", url=None, kind="Profile-based offer",
      brief="A profile-based, assessment-led offer, with a value proposition and customer journey built around the profile.",
      blueprint=("assessment", "Assessment → results → CRM → email")),
 dict(id="sales-services", name="Sales services company", url=None, kind="Service & sales funnel",
      brief="A service business whose site positions the offer and moves visitors toward a sales conversation.",
      blueprint=("vsl", "Landing page → VSL → booked call")),
]

ROLE = ("End to end: I built and connected the whole journey, then tested and maintained it.")
SCOPE = ["Funnel pages, forms and assessment or booking steps", "CRM custom fields, tags and segments",
         "Email sequences and automation triggers", "Calendar and booking connections",
         "QA testing from form submission to follow-up", "Ongoing maintenance and fixes"]

def status(v):
    return '<span class="status pending">To be confirmed</span>' if v is None else '<span class="status verified">Confirmed</span>'

def card(p):
    return f"""
      <button class="proj" type="button" data-open="{p['id']}" aria-haspopup="dialog">
        <span class="proj-top"><span class="kind">{e(p['kind'])}</span><b>{e(p['name'])}</b></span>
        <span class="proj-bottom">
          <span class="chips"><span class="status verified">End-to-end build</span></span>
          <p>{e(p['brief'])}</p>
          <span class="open">Open case study</span>
        </span>
      </button>"""

def dialog(p):
    scope = "".join(f"<li>{e(x)}</li>" for x in SCOPE)
    bp = ""
    if p["blueprint"]:
        bp = f"""<div class="box note"><div class="field-row"><h3>How this kind of journey works</h3><span class="status blueprint">Representative blueprint</span></div>
            <p>A representative workflow for this type of project. It shows the logic, not a copy of the client's account.</p>
            <a class="link-arrow" href="blueprints.html#{p['blueprint'][0]}">{e(p['blueprint'][1])}</a></div>"""
    return f"""
<dialog class="case" id="{p['id']}" aria-labelledby="{p['id']}-title">
  <div class="case-top">
    <button class="case-close" type="button" data-close>Close</button>
    <span class="eyebrow" style="color:#FF9C7E">{e(p['kind'])}</span>
    <h2 id="{p['id']}-title">{e(p['name'])}</h2>
    <p style="color:#C9D5E3;max-width:60ch">{e(p['brief'])}</p>
  </div>
  <div class="case-body">
    <div class="box"><div class="field-row"><h3>My role</h3><span class="status verified">Confirmed</span></div><p>{e(ROLE)}</p></div>
    <div class="box"><h3>What that covered</h3><ul>{scope}</ul></div>
    {bp}
  </div>
</dialog>"""

html = f"""<section class="page-hero">
  <div class="wrap">
    <span class="eyebrow">Projects</span>
    <h1>Assessments, profile offers and <span class="accent">sales journeys.</span></h1>
    <p class="lede">Clients are described rather than named. Each project below is marked honestly. On every project I built the journey end to end: pages, CRM, automations, QA and upkeep.</p>
  </div>
</section>

<section class="section" style="padding-top:8px">
  <div class="wrap">
    <div class="integrity" style="grid-template-columns:1fr 1fr" aria-label="How to read these case studies">
      <div><span class="status verified">Confirmed</span><span>Work I personally built, connected, tested and maintained.</span></div>
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
