"""Generates src/systems/pages/index.html, the one-page systems portfolio.

Rules (see FACTS.md): clients are described, not named; Fran built every client build end to end;
build descriptions use only what is visible on the supplied screenshots. Run this, then
scripts/build_systems.py.
"""
from pathlib import Path
from html import escape as e

# Five build types shown as flow charts. A step marked with * is the CRM hub (highlighted).
FLOWS = [
    dict(id="assessment", name="Assessment",
         steps=["Landing page", "Questions", "Lead capture", "*CRM fields & tags", "Results page", "Results email", "Nurture", "Book a call"],
         notes=["Each answer saved to its own CRM field", "Outcome tag decides the result and the follow-up", "Every result path tested before launch"]),
    dict(id="masterclass", name="Masterclass",
         steps=["Event page", "Registration", "*CRM tag", "Confirmation", "Reminders", "Live event", "Replay", "Offer"],
         notes=["Reminders timed to the event, in the registrant's time zone", "Attended and missed get different follow-up", "Buyers stop receiving offer emails"]),
    dict(id="book-a-call", name="Book a call",
         steps=["Sales page", "VSL", "Booking calendar", "*CRM & pipeline", "Confirmation", "Reminders", "Call", "Follow-up"],
         notes=["One contact per booking, no duplicates", "Separate paths for attended, no-show and rescheduled", "Whoever takes the call is notified with the intake answers"]),
    dict(id="application", name="Application",
         steps=["Application page", "Multi-step form", "*CRM fields", "Review", "Qualified", "Book a call", "Reminders", "Sales call"],
         notes=["Contact details captured on step one, so incomplete applications can be followed up", "Automatic or manual qualification, depending on the business", "Only qualified applicants get the booking link"]),
    dict(id="lead-gathering", name="Lead gathering",
         steps=["Opt-in page", "Form", "*CRM tags", "Asset delivery", "Welcome", "Nurture", "Offer", "Converted"],
         notes=["Source and interest tagged on sign-up", "Free resource delivered instantly", "Nurture stops as soon as someone converts"]),
]

BUILT = {
    "assessment": ["Landing page and calls to action", "Question flow and lead capture", "Results logic and personalised report or results page",
                   "CRM fields, tags and segments", "Results email and follow-up sequence", "QA and ongoing maintenance"],
    "book-a-call": ["Sales page and booking calls to action", "Booking calendar and intake questions", "CRM contact and pipeline updates",
                    "Confirmation and reminder emails", "No-show and rescheduling follow-up", "QA and ongoing maintenance"],
}

PROJECTS = [
    dict(id="board-assessment", flow="assessment", img="board-assessment", w=526,
         name="Non-profit board effectiveness assessment", kind="Leadership consultant",
         summary="A 10-minute diagnostic for non-profit executive directors and CEOs. It scores the board across nine pillars and delivers a personalised report.",
         seen=["Hero with a 'Take the assessment' call to action, repeated down the page", "'What you'll walk away with' section showing the personalised report",
               "Three-step 'How it works'", "Nine measured pillars, each explained"]),
    dict(id="courage-assessment", flow="assessment", img="courage-assessment", w=550,
         name="Courage profile assessment", kind="Speaker & author",
         summary="Sixteen questions, about four minutes. People find out which of nine courage types they are and receive a personalised profile report.",
         seen=["Nine type cards introducing each result", "What the assessment report includes", "Three-step path from questions to profile",
               "'Find your courage type' call to action throughout"]),
    dict(id="relationship-diagnostic", flow="assessment", img="relationship-diagnostic", w=308,
         name="Relationship pattern diagnostic", kind="Women's relationship coach",
         summary="A diagnostic for women whose love life hasn't matched the rest of their life, leading to a written portrait of the pattern behind it.",
         seen=["Hero with a single assessment call to action", "Three-step 'How it works'", "Symptom sections that lead into the diagnostic",
               "Description of the written portrait each person receives"]),
    dict(id="four-worlds-assessment", flow="assessment", img="four-worlds-assessment", w=602,
         name="Four-worlds inner map assessment", kind="Personal development",
         summary="A ten-minute assessment that shows which of four positions a person lives in, with one calibrated next step chosen for them.",
         seen=["Four-image hero with 'Start the assessment'", "What people receive on completion", "Founder story section",
               "'Ten minutes, taken honestly' framing before the start"]),
    dict(id="pattern-profile", flow="assessment", img="pattern-profile", w=328,
         name="Emotional pattern profile", kind="Personal development",
         summary="A profile completed in under ten minutes that names a person's emotional pattern and scores how they respond, with a roadmap for what to do next.",
         seen=["Problem-led hero with one profile call to action", "'Does this sound familiar?' symptom cards",
               "Breakdown of what the profile report contains", "Repeated calls to take the profile"]),
    dict(id="sales-talent-booking", flow="book-a-call", img="sales-talent-booking", w=389,
         name="Fractional sales talent agency", kind="B2B services",
         summary="A sales page for placing fractional closers and account executives, built to move business owners toward a booked call.",
         seen=["'Schedule a call now' calls to action throughout the page", "Step-by-step roadmap and transparent pricing tiers",
               "An opt-in form to view sample candidates before booking", "Frequently asked questions and a recruitment call to action"]),
]

ROLE = "End to end: I built and connected the whole journey, then tested and maintained it."


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
    built = "".join(f"<li>{e(x)}</li>" for x in BUILT[p["flow"]])
    seen = "".join(f"<li>{e(x)}</li>" for x in p["seen"])
    return f"""
<dialog class="case" id="{p['id']}" aria-labelledby="{p['id']}-title">
  <div class="case-top">
    <button class="case-close" type="button" data-close>Close</button>
    <span class="eyebrow" style="color:#FF9C7E">{e(p['kind'])}</span>
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
      <a class="link-arrow" href="#funnels" data-flow="{p['flow']}">See how this kind of funnel flows</a>
    </div>
  </div>
</dialog>"""


def flow_panel(f, first):
    pills = []
    for i, st in enumerate(f["steps"]):
        hub = st.startswith("*")
        pills.append(f'<li class="pill{" crm" if hub else ""}">{e(st.lstrip("*"))}</li>')
    notes = "".join(f"<li>{e(n)}</li>" for n in f["notes"])
    return f"""
      <div class="flow-panel" id="flow-{f['id']}" role="tabpanel" aria-labelledby="ftab-{f['id']}"{"" if first else " hidden"}>
        <ol class="pills">{"".join(pills)}</ol>
        <ul class="flow-notes">{notes}</ul>
      </div>"""


tabs = "".join(
    f'<button role="tab" id="ftab-{f["id"]}" aria-controls="flow-{f["id"]}" aria-selected="{"true" if i == 0 else "false"}" tabindex="{0 if i == 0 else -1}" type="button">{e(f["name"])}</button>'
    for i, f in enumerate(FLOWS))

TOOLS = [
    ("Marketing, CRM & automation", ["GoHighLevel", "HubSpot", "Kajabi", "Kit (ConvertKit)", "Kartra", "Ahrefs", "Google Analytics",
                                     "Google Search Console", "Instagram", "LinkedIn", "Pinterest", "Substack"]),
    ("Web, development & deployment", ["Vercel", "GitHub", "Git", "Neon", "Claude Code", "Wix", "HTML", "CSS", "JavaScript"]),
    ("AI & automation", ["Claude", "ChatGPT (OpenAI)", "Prompt engineering", "AI-assisted content", "Workflow automation"]),
    ("Data & analytics", ["Google Sheets", "Microsoft Excel", "Airtable", "SQL (basic)", "Neon (PostgreSQL)"]),
    ("Productivity & operations", ["Google Workspace", "Slack", "Zoom", "Notion", "Airtable"]),
    ("Design & content", ["Canva", "Figma", "CapCut", "Loom"]),
    ("Business & client operations", ["Client onboarding", "Reporting & dashboards", "Automated messaging", "Funnel building",
                                      "Sales pipeline management", "SOPs & documentation"]),
]
tools = "".join(f'<div><h3>{e(c)}</h3><div class="chips">{"".join(f"<span class=\"chip\">{e(t)}</span>" for t in ts)}</div></div>' for c, ts in TOOLS)

html = f"""<section class="hero" id="intro">
  <div class="wrap">
    <div>
      <span class="eyebrow">Funnel builder · CRM &amp; marketing automation</span>
      <h1>Funnels, CRM &amp; automations that <span class="accent">work together.</span></h1>
      <p class="lede">I build assessment, masterclass, book-a-call, application and lead gathering funnels, and connect them to your CRM and email, so every lead reaches the right next step.</p>
      <div class="btn-row">
        <a class="btn btn-primary" href="#builds">See my builds</a>
        <a class="btn btn-ghost" href="#contact">Let's talk</a>
      </div>
      <p class="hero-note">15 years of professional experience · remote since 2016 · also see my <a href="../socialmedia/">social media portfolio</a></p>
    </div>
    <figure class="sysmap" aria-label="How the system connects">
      <div class="sysmap-grid">
        <div class="sysmap-col">
          <div class="node"><b>Landing page</b><span>opt-in · VSL</span></div>
          <div class="node"><b>Assessment</b><span>questions · result</span></div>
          <div class="node"><b>Registration</b><span>masterclass</span></div>
        </div>
        <svg class="wires" viewBox="0 0 46 240" preserveAspectRatio="none" aria-hidden="true">
          <path d="M0 40 C 26 40, 20 120, 46 120"/><path d="M0 120 L 46 120"/><path d="M0 200 C 26 200, 20 120, 46 120"/><path class="pulse" d="M0 120 L 46 120"/>
        </svg>
        <div class="down" aria-hidden="true">↓</div>
        <div class="hub"><span class="mono" style="font-size:11px;letter-spacing:.08em;color:#FF9C7E">THE HUB</span><b>CRM</b>
          <div class="chips"><span class="chip">fields</span><span class="chip">tags</span><span class="chip">pipeline</span></div></div>
        <svg class="wires" viewBox="0 0 46 240" preserveAspectRatio="none" aria-hidden="true">
          <path d="M0 120 C 26 120, 20 40, 46 40"/><path d="M0 120 L 46 120"/><path d="M0 120 C 26 120, 20 200, 46 200"/><path class="pulse" d="M0 120 C 26 120, 20 40, 46 40"/>
        </svg>
        <div class="down" aria-hidden="true">↓</div>
        <div class="sysmap-col">
          <div class="node out"><b>Email automation</b><span>nurture · reminders</span></div>
          <div class="node out"><b>Booking calendar</b><span>confirm · no-show</span></div>
          <div class="node goal"><b>Sales conversation</b><span>call · enrol · buy</span></div>
        </div>
      </div>
    </figure>
  </div>
</section>

<section class="section alt" id="builds">
  <div class="wrap">
    <div class="sec-head">
      <div><span class="eyebrow">Client builds</span><h2 style="margin-top:12px">Six funnels I built end to end</h2></div>
      <p class="lede">Pages, CRM setup, automations, testing and upkeep. Hover a build to scroll its page, or open it for details. Clients are described rather than named.</p>
    </div>
    <div class="proj-grid">{"".join(card(p) for p in PROJECTS)}
    </div>
  </div>
</section>

<section class="section" id="funnels">
  <div class="wrap">
    <div class="sec-head">
      <div><span class="eyebrow">How each funnel flows</span><h2 style="margin-top:12px">Five builds, one connected system</h2></div>
      <p class="lede">Pick a funnel to see its steps. The coral step is the CRM, where every contact is stored and sorted so the right follow-up happens.</p>
    </div>
    <div class="tabs" role="tablist" aria-label="Funnel types">{tabs}</div>
    <div class="flows">{"".join(flow_panel(f, i == 0) for i, f in enumerate(FLOWS))}
    </div>
  </div>
</section>

<section class="section dark" id="services">
  <div class="wrap">
    <div class="sec-head">
      <div><span class="eyebrow">Services</span><h2 style="margin-top:12px">What I take care of</h2></div>
      <p class="lede">I work inside your existing tools or set up new ones, and make sure the pieces talk to each other.</p>
    </div>
    <div class="svc-grid">
      <div><b>Funnel building</b><span>Landing, opt-in, assessment, booking, masterclass and application pages, plus thank-you pages and follow-up.</span></div>
      <div><b>CRM setup &amp; integration</b><span>Custom fields, tags, segments, pipelines and lead sources, with forms and calendars mapped correctly.</span></div>
      <div><b>Email automation</b><span>Welcome, results, nurture, reminder, no-show, replay and onboarding sequences with the right triggers and exits.</span></div>
      <div><b>QA &amp; systems support</b><span>Testing every path before launch, troubleshooting broken links and triggers, and documenting how it all works.</span></div>
    </div>
  </div>
</section>

<section class="section" id="tools">
  <div class="wrap two-col">
    <div><span class="eyebrow">Tools &amp; tech stack</span><h2 style="margin-top:12px">Give me the tool or software, and <span class="accent">I'll make it work.</span></h2><p class="lede" style="margin-top:14px">I'm a fast learner and highly adaptable. This is a selection of the tools I've worked with, not a limit. If there's a new system, I'll get up to speed.</p></div>
    <div class="tool-rows">{tools}</div>
  </div>
</section>

<section class="section alt" id="about">
  <div class="wrap two-col">
    <div><span class="eyebrow">About</span><h2 style="margin-top:12px">Marketing, tech and operations in one person</h2></div>
    <div class="prose">
      <p>I'm Fran, a remote professional with 15 years of experience in digital marketing implementation, CRM workflows, funnel building, email marketing, website management and business operations. I've worked remotely since 2016, from the Philippines.</p>
      <p>I think about the whole journey: what happens when someone fills in a form, where their details are stored, which tags and fields drive the follow-up, and what should happen if they book, miss a call or buy. When something breaks, I trace it step by step until it works again.</p>
    </div>
  </div>
</section>

<section class="section" id="contact">
  <div class="wrap">
    <div class="cta-band">
      <div><h2>Let's map your customer journey.</h2><p>Tell me what you're building and the tools you use. I'll reply by email.</p>
        <p class="email-big"><a href="mailto:fran.f.crystal@gmail.com" id="email-addr">fran.f.crystal@gmail.com</a></p></div>
      <button class="btn" type="button" data-copy="fran.f.crystal@gmail.com" data-target="email-addr">Copy email</button>
    </div>
  </div>
</section>
{"".join(dialog(p) for p in PROJECTS)}
"""
out = Path(__file__).resolve().parent.parent / "pages" / "index.html"
out.write_text(html)
print("wrote", out)
