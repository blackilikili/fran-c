"""Generates src/systems/pages/blueprints.html from the funnel data below."""
from pathlib import Path
from html import escape as e

FUNNELS_RAW = [
 dict(id="assessment", tab="Assessment", title="Assessment funnel: questions → personalised results → CRM → email",
  intro="A personality profile, readiness check or business diagnostic that captures answers, classifies an outcome and sends each person down the follow-up that matches their result.",
  systems=["Landing page", "Assessment tool", "CRM", "Email automation", "Calendar"],
  steps=[("Traffic","Traffic or referral"),("Page","Assessment landing page"),("Form","Assessment questions"),("Form","Lead capture: name and email"),
         ("CRM","Answers mapped to CRM fields"),("Logic","Scoring or outcome classification",1),("Page","Personalised results page"),("CRM","Outcome tags and segment"),
         ("Email","Results delivery email"),("Email","Outcome-specific nurture"),("Calendar","Relevant offer or booking CTA",1),("CRM","Follow-up and lead tracking")],
  branch=("Outcome assigned",[("Outcome A","Result A page and email, nurture A, CTA matched to A."),("Outcome B","Result B page and email, nurture B, CTA matched to B."),("Outcome C","Result C page and email, nurture C, CTA matched to C."),("Started, not finished","Partial-completion reminder, only if contact details were captured first.")]),
  logic=["Capture contact details and every answer.","Map each answer to its own CRM field.","Assign the outcome using the assessment's rules.","Apply the matching outcome tag or segment.","Show or send the correct result.","Trigger the matching sequence only once (guard against duplicate enrolment).","Exit the nurture when the person books or buys."],
  qa=["Complete the assessment once per outcome with a test contact.","Check fields, tags and workflow enrolment on each test record.","Retake with the same email: confirm no duplicate contact or second sequence.","Check every result link and booking link."],
  note="Automatic scoring calculates the outcome instantly. Manual review holds the result until a person checks the answers, then a tag or field change releases the right email. They're built differently, so I confirm which one the business uses first.",
  cta=("Discuss an assessment funnel","contact.html")),
 dict(id="vsl", tab="Book a call", title="Book-a-call funnel: landing page → VSL → booked call → follow-up",
  intro="A sales page with a video sales letter that moves interested people to a booked call, with the CRM and reminders handling everything around the appointment.",
  systems=["Landing page", "Video", "Booking calendar", "CRM / pipeline", "Email & SMS reminders"],
  steps=[("Traffic","Traffic or referral"),("Page","Sales landing page"),("Page","Video sales letter"),("Page","CTA: book a call",1),("Calendar","Booking calendar with intake questions"),("Email","Booking confirmation"),
         ("CRM","Contact and opportunity created"),("Email","Appointment reminders"),("Email","Pre-call nurture"),("Calendar","Call: attended, cancelled or no-show",1),("Email","Outcome-specific follow-up"),("CRM","Pipeline stage updated")],
  branch=("After the call time",[("Attended","Notes logged, opportunity moves to the next stage, post-call follow-up starts."),("No-show","No-show email with a rebook link; opportunity flagged for the closer."),("Cancelled","Reschedule invitation; reminders for the old time are stopped."),("Rescheduled","Reminders reset to the new time; one record, no duplicates.")]),
  logic=["Calendar connected to the CRM so a booking creates or updates one contact.","Lead source and intake answers saved to fields.","Confirmation sent immediately; reminders timed relative to the appointment.","Internal notification to whoever takes the call.","Pipeline stage changes on booking, attendance and outcome, where a pipeline is configured."],
  qa=["Book, reschedule and cancel with a test contact.","Check reminder timing in two different time zones.","Mark a test call as no-show and confirm the right sequence starts.","Confirm the closer receives the notification with the intake answers."],
  note="This journey is where marketing hands over to sales. The aim is that the person taking the call already has the context, and nobody falls through the gap between booked and attended.",
  cta=("See how I'd set up your booking flow","contact.html")),
 dict(id="masterclass", tab="Masterclass", title="Masterclass funnel: registration → reminders → live event → replay → offer",
  intro="From promotion to replay: registration, reminders in the right time zone, attendance-based follow-up and a clear next step after the event.",
  systems=["Event page", "Registration form", "CRM", "Email automation", "Zoom or event platform"],
  steps=[("Page","Promotional landing page"),("Form","Registration form"),("CRM","Contact created or updated"),("CRM","Event registration tag"),("Email","Confirmation with joining details"),("Calendar","Add-to-calendar link"),
         ("Email","Reminder sequence"),("Event","Live event",1),("CRM","Attendance classification, where available"),("Email","Replay email"),("Email","Follow-up nurture"),("Calendar","Offer or booking CTA",1)],
  branch=("After the event",[("Attended","Thank-you, key takeaways and the offer while it's fresh."),("Registered, didn't attend","Replay email with a deadline; reminders to watch."),("Attended, no next step","Shorter nurture answering common objections."),("Clicked offer or booked","Leaves the event follow-up and moves to sales or onboarding, where tracking is available.")]),
  logic=["Event date and time stored once and reused, so changes update everywhere.","Reminders timed from the event, displayed in the registrant's time zone where the tools allow.","Registration tag per event, so past registrants aren't messaged about the wrong session.","Attendance data imported or synced after the event, where the platform provides it.","Replay access closed or redirected after the deadline."],
  qa=["Register test contacts in different time zones.","Check each reminder's send time and joining link.","Simulate attended and not-attended contacts after the event.","Confirm buyers stop receiving the offer emails."],
  note="If the event platform doesn't report attendance, everyone receives the replay version. I'd say so plainly rather than pretend the follow-up is more personalised than it is.",
  cta=("Explore event systems","contact.html")),
 dict(id="leadmagnet", tab="Lead gathering", title="Lead gathering funnel: opt-in → CRM → nurture → conversion",
  intro="A free resource that brings people in, delivers what was promised immediately, then nurtures them toward one clear next step, and stops when they take it.",
  systems=["Opt-in page", "Form", "CRM", "Email automation"],
  steps=[("Page","Lead magnet landing page"),("Form","Opt-in form"),("CRM","Contact captured"),("CRM","Source and interest tags"),("Email","Asset delivery",1),("Email","Welcome sequence"),
         ("Email","Educational nurture"),("CRM","Engagement-based segment, where configured"),("Page","Relevant offer"),("Calendar","Book, apply or buy",1)],
  branch=("During the nurture",[("Converts","Exits immediately; moves to the booking, application or customer journey."),("Engaged, not converted","Continues nurture; may get a more direct offer."),("Not engaging","Moves to a lighter re-engagement path, or is suppressed.")]),
  logic=["Deliver the asset instantly, with a backup link in case the email is filtered.","Tag the source and the topic of interest.","Goal or exit condition on every nurture: booked, applied or purchased.","Suppress contacts already in a sales or customer journey.","Avoid re-sending the welcome sequence when someone opts in a second time."],
  qa=["Opt in with a new email and an existing one.","Check the delivery email and the download link.","Trigger the conversion action and confirm the nurture stops."],
  note="The most common gap I see here is the missing exit: people keep receiving 'ready to start?' emails after they've already bought.",
  cta=("Get help with your nurture sequence","contact.html")),
 dict(id="application", tab="Application", title="Application funnel: multi-step application → review → qualified call",
  intro="For high-ticket offers: a multi-step application that captures the right information, routes each applicant appropriately and only invites qualified people to book.",
  systems=["Application page", "Multi-step form", "CRM", "Email", "Booking calendar"],
  steps=[("Page","Application landing page"),("Form","Multi-step application"),("CRM","Contact and application data captured"),("CRM","Segment by answers"),("Logic","Qualification rules or manual review",1),("Email","Internal notification"),
         ("Email","Booking invitation for qualified leads"),("Calendar","Booking confirmation and reminders"),("Calendar","Sales conversation",1),("CRM","Follow-up and pipeline progress")],
  branch=("After the application",[("Qualified","Invitation to book, with confirmation and reminders."),("Not a fit right now","Kind decline, plus a lower-commitment resource or offer."),("Incomplete","Reminder to finish, if contact details were captured on step one."),("Needs review","Held for a person to decide; status field updated when they do.")]),
  logic=["Capture contact details on the first step so incomplete applications can be followed up.","Store each answer in its own field for review and reporting.","Automatic qualification only where clear rules have been agreed; otherwise manual review.","Booking link sent only to qualified applicants.","Status field records the decision, so reporting stays accurate."],
  qa=["Submit one qualified, one unqualified and one incomplete test application.","Confirm each lands in the right segment and gets the right email.","Check the reviewer's notification includes the answers."],
  note="I don't assume automated qualification. Many businesses review applications by hand, and the system should support that rather than guess.",
  cta=("Discuss your application funnel","contact.html"))
]

ORDER = ["assessment", "masterclass", "vsl", "application", "leadmagnet"]
FUNNELS = sorted(FUNNELS_RAW, key=lambda f: ORDER.index(f["id"]))

def chip(layer): return f'<span class="chip layer">{e(layer)}</span>'

def panel(f, i):
    steps = "".join(
        f'<li{" class=\"key\"" if len(s) > 2 else ""}>{chip(s[0])}<b>{e(s[1])}</b></li>' for s in f["steps"])
    src, branches = f["branch"]
    br = "".join(f'<div class="branch"><h4>{e(t)}</h4><p>{e(d)}</p></div>' for t, d in branches)
    logic = "".join(f"<li>{e(x)}</li>" for x in f["logic"])
    qa = "".join(f"<li>{e(x)}</li>" for x in f["qa"])
    systems = "".join(f'<span class="chip">{e(s)}</span>' for s in f["systems"])
    return f"""
  <section class="bp" id="{f['id']}" role="tabpanel" aria-labelledby="tab-{f['id']}">
    <div class="bp-head">
      <div><span class="eyebrow">Blueprint {i:02d}</span><h2 style="margin-top:10px">{e(f['title'])}</h2></div>
      <div class="meta"><p class="muted">{e(f['intro'])}</p><div class="chips">{systems}</div></div>
    </div>
    <div>
      <h3 class="sr">Journey steps</h3>
      <ol class="flow">{steps}</ol>
    </div>
    <div class="branches">
      <h3 class="sr">Branches</h3>
      <div class="branch-src">{e(src)}</div>
      <div class="branch-row" style="--n:{len(branches)}">{br}</div>
    </div>
    <div class="bp-cols">
      <div class="box"><h3>Operational logic</h3><ul>{logic}</ul></div>
      <div class="box"><h3>What I test before launch</h3><ul>{qa}</ul></div>
    </div>
    <div class="box note"><p>{e(f['note'])}</p><div><a class="link-arrow" href="{f['cta'][1]}">{e(f['cta'][0])}</a></div></div>
  </section>"""

tabs = "".join(
    f'<button role="tab" id="tab-{f["id"]}" aria-controls="{f["id"]}" aria-selected="{"true" if i == 0 else "false"}" type="button">{e(f["tab"])}</button>'
    for i, f in enumerate(FUNNELS))
html = f"""<section class="page-hero">
  <div class="wrap">
    <span class="eyebrow">Systems &amp; funnel blueprints</span>
    <h1>Five builds, mapped <span class="accent">end to end.</span></h1>
    <p class="lede">Each blueprint shows the steps a person goes through, the system behind each step, how the journey branches and what I check before it goes live. These are representative builds, not diagrams of a specific client's account.</p>
    <div class="chips" style="margin-top:20px"><span class="status blueprint">Representative blueprints</span></div>
  </div>
</section>

<section class="section" style="padding-top:8px">
  <div class="wrap">
    <div class="tabs" role="tablist" aria-label="Funnel blueprints">{tabs}</div>
{"".join(panel(f, i + 1) for i, f in enumerate(FUNNELS))}
    <div class="cta-band">
      <div><h2>Your journey probably looks like a mix of these.</h2><p>Send me the steps you have now and where people drop off. I'll map what the system should be doing.</p></div>
      <a class="btn" href="contact.html">Let's map your customer journey</a>
    </div>
  </div>
</section>
"""
out = Path(__file__).resolve().parent.parent / "pages" / "blueprints.html"
out.write_text(html)
print("wrote", out)
