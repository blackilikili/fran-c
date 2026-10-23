"""Generates src/systems/pages/projects.html: client builds grouped by build type.

Integrity rules: clients are described, not named. Fran confirmed she built each project end to end.
Descriptions only use what is visible on the supplied page screenshots. Build types with no supplied
client sample show the representative blueprint and say samples are available on request.
Re-run this script, then scripts/build_systems.py.
"""
from pathlib import Path
from html import escape as e

TYPES = [
    dict(id="assessment", name="Assessment funnels", blueprint="assessment",
         lede="Question flows that capture answers, produce a personalised result or report, and start the follow-up that matches it.",
         built=["Landing page and calls to action", "Question flow and lead capture", "Results logic and personalised report or results page",
                "CRM fields, tags and segments for each answer and outcome", "Results email and follow-up sequence", "End-to-end QA and ongoing maintenance"]),
    dict(id="masterclass", name="Masterclass funnels", blueprint="masterclass",
         lede="Registration pages, confirmation and reminder emails, replay delivery and post-event follow-up.",
         built=["Registration page and form", "CRM registration tags", "Confirmation, joining details and reminders",
                "Replay delivery", "Attended and not-attended follow-up", "QA across time zones"]),
    dict(id="book-a-call", name="Book-a-call funnels", blueprint="vsl",
         lede="Sales pages that move interested people to a booked call, with confirmations, reminders and follow-up around the appointment.",
         built=["Sales landing page and booking calls to action", "Booking calendar and intake questions", "CRM contact and pipeline updates",
                "Confirmation and reminder emails", "No-show and rescheduling follow-up", "End-to-end QA and ongoing maintenance"]),
    dict(id="application", name="Application funnels", blueprint="application",
         lede="Multi-step applications that capture the right information and route qualified people to a call.",
         built=["Application page and multi-step form", "Answers saved to CRM fields", "Review or qualification routing",
                "Internal notifications", "Booking invitation for qualified applicants", "Incomplete-application follow-up"]),
    dict(id="lead-gathering", name="Lead gathering funnels", blueprint="leadmagnet",
         lede="Opt-in pages and lead magnets that capture contacts, tag them by source and interest, and nurture them toward the next step.",
         built=["Opt-in page and form", "Source and interest tagging", "Instant asset delivery",
                "Welcome and nurture sequence", "Exit once the person converts", "QA of capture and delivery"]),
]

PROJECTS = [
    dict(id="board-assessment", type="assessment", img="board-assessment", w=526,
         name="Non-profit board effectiveness assessment", kind="Leadership consultant",
         summary="A 10-minute diagnostic for non-profit executive directors and CEOs. It scores the board across nine pillars and delivers a personalised report.",
         seen=["Hero with a 'Take the assessment' call to action, repeated down the page", "'What you'll walk away with' section showing the personalised report",
               "Three-step 'How it works'", "Nine measured pillars, each explained"]),
    dict(id="courage-assessment", type="assessment", img="courage-assessment", w=550,
         name="Courage profile assessment", kind="Speaker & author",
         summary="Sixteen questions, about four minutes. People find out which of nine courage types they are and receive a personalised profile report.",
         seen=["Nine type cards introducing each result", "What the assessment report includes", "Three-step path from questions to profile",
               "'Find your courage type' call to action throughout"]),
    dict(id="relationship-diagnostic", type="assessment", img="relationship-diagnostic", w=308,
         name="Relationship pattern diagnostic", kind="Women's relationship coach",
         summary="A diagnostic for women whose love life hasn't matched the rest of their life, leading to a written portrait of the pattern behind it.",
         seen=["Hero with a single assessment call to action", "Three-step 'How it works'", "Symptom sections that lead into the diagnostic",
               "Description of the written portrait each person receives"]),
    dict(id="four-worlds-assessment", type="assessment", img="four-worlds-assessment", w=602,
         name="Four-worlds inner map assessment", kind="Personal development",
         summary="A ten-minute assessment that shows which of four positions a person lives in, with one calibrated next step chosen for them.",
         seen=["Four-image hero with 'Start the assessment'", "What people receive on completion", "Founder story section",
               "'Ten minutes, taken honestly' framing before the start"]),
    dict(id="pattern-profile", type="assessment", img="pattern-profile", w=328,
         name="Emotional pattern profile", kind="Personal development",
         summary="A profile completed in under ten minutes that names a person's emotional pattern and scores how they respond, with a roadmap for what to do next.",
         seen=["Problem-led hero with one profile call to action", "'Does this sound familiar?' symptom cards",
               "Breakdown of what the profile report contains", "Repeated calls to take the profile"]),
    dict(id="sales-talent-booking", type="book-a-call", img="sales-talent-booking", w=389,
         name="Fractional sales talent agency", kind="B2B services",
         summary="A sales page for placing fractional closers and account executives, built to move business owners toward a booked call.",
         seen=["'Schedule a call now' calls to action throughout the page", "Step-by-step roadmap and transparent pricing tiers",
               "An opt-in form to view sample candidates before booking", "Frequently asked questions and a recruitment call to action"]),
]

ROLE = "End to end: I built and connected the whole journey, then tested and maintained it."


def type_of(tid):
    return next(t for t in TYPES if t["id"] == tid)


def card(p):
    return f"""
        <button class="proj shot" type="button" data-open="{p['id']}" aria-haspopup="dialog">
          <span class="frame"><span class="bar" aria-hidden="true"><i></i><i></i><i></i></span>
            <span class="page" role="img" aria-label="Full-page screenshot of the {e(p['name'].lower())} landing page" style="background-image:url('img/{p['img']}.jpg')"></span></span>
          <span class="proj-bottom">
            <span class="kind-line">{e(p['kind'])}</span>
            <b class="proj-name">{e(p['name'])}</b>
            <p>{e(p['summary'])}</p>
            <span class="open">Open the build</span>
          </span>
        </button>"""


def dialog(p):
    t = type_of(p["type"])
    built = "".join(f"<li>{e(x)}</li>" for x in t["built"])
    seen = "".join(f"<li>{e(x)}</li>" for x in p["seen"])
    return f"""
<dialog class="case" id="{p['id']}" aria-labelledby="{p['id']}-title">
  <div class="case-top">
    <button class="case-close" type="button" data-close>Close</button>
    <span class="eyebrow" style="color:#FF9C7E">{e(t['name'][:-1])} · {e(p['kind'])}</span>
    <h2 id="{p['id']}-title">{e(p['name'])}</h2>
    <p style="color:#C9D5E3;max-width:60ch">{e(p['summary'])}</p>
  </div>
  <div class="case-body case-split">
    <div class="scroller" tabindex="0" aria-label="Scrollable full-page screenshot">
      <img src="img/{p['img']}.jpg" width="{p['w']}" height="2000" alt="Full landing page of the {e(p['name'].lower())}" loading="lazy">
    </div>
    <div class="stack" style="gap:16px">
      <div class="box"><div class="field-row"><h3>My role</h3><span class="status verified">Confirmed</span></div><p>{e(ROLE)}</p></div>
      <div class="box"><h3>What I built</h3><ul>{built}</ul></div>
      <div class="box"><h3>On the page</h3><ul>{seen}</ul></div>
      <a class="link-arrow" href="blueprints.html#{t['blueprint']}">See the {e(t['name'][:-1].lower())} blueprint</a>
    </div>
  </div>
</dialog>"""


def section(t):
    projects = [p for p in PROJECTS if p["type"] == t["id"]]
    count = f"{len(projects)} client build{'s' if len(projects) != 1 else ''}" if projects else "Blueprint"
    if projects:
        body = f'<div class="proj-grid">{"".join(card(p) for p in projects)}\n      </div>'
    else:
        body = f"""<div class="box note type-empty">
          <p>Client examples of this build are available on request. The blueprint shows how I set it up, step by step.</p>
          <div class="btn-row"><a class="btn btn-dark" href="blueprints.html#{t['blueprint']}">See the blueprint</a><a class="btn btn-ghost" href="contact.html">Ask for examples</a></div>
        </div>"""
    return f"""
    <section class="type-sec" id="{t['id']}" aria-labelledby="{t['id']}-h">
      <div class="type-head">
        <div><span class="eyebrow">{count}</span><h2 id="{t['id']}-h">{e(t['name'])}</h2></div>
        <div class="stack"><p class="lede">{e(t['lede'])}</p>{'<a class="link-arrow" href="blueprints.html#' + t['blueprint'] + '">See the blueprint</a>' if projects else ''}</div>
      </div>
      {body}
    </section>"""


jump = "".join(f'<a href="#{t["id"]}">{e(t["name"].replace(" funnels", ""))}</a>' for t in TYPES)
html = f"""<section class="page-hero">
  <div class="wrap">
    <span class="eyebrow">Builds</span>
    <h1>Assessment, masterclass, booking, application and <span class="accent">lead funnels.</span></h1>
    <p class="lede">Client builds grouped by type. On every one I built the journey end to end: pages, CRM, automations, QA and upkeep. Clients are described rather than named.</p>
    <nav class="jump" aria-label="Build types">{jump}</nav>
  </div>
</section>

<section class="section" style="padding-top:8px">
  <div class="wrap">{"".join(section(t) for t in TYPES)}
    <div class="cta-band" style="margin-top:24px">
      <div><h2>Which build does your business need?</h2><p>Tell me about your offer and the tools you use. I'll suggest the right funnel and how I'd connect it.</p></div>
      <a class="btn" href="contact.html">Discuss your funnel build</a>
    </div>
  </div>
</section>
{"".join(dialog(p) for p in PROJECTS)}
"""
out = Path(__file__).resolve().parent.parent / "pages" / "projects.html"
out.write_text(html)
print("wrote", out)
