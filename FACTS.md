# Confirmed facts and open questions

Source of truth: `BRIEF.md` plus Fran's answers in the working session. Only items under "Confirmed" go into portfolio copy as claims.

## Confirmed

- Display name Fran C.; contact fran.f.crystal@gmail.com; Philippines; remote. No LinkedIn.
- Target roles: Social Media Manager, Content Editor, Content Marketing.
- 15 years of professional experience; remote since 2016 (both confirmed exact by Fran).
- Tagline: "A content creator with an operations background: 15 years of making sure good work actually ships."
- **Helen Millar (Helen Heart Healer + The Hearty Company):** Fran does all of it: designs the post layouts, makes the posts, writes captions, schedules and publishes. Evidence: Heart Healer Facebook post "Published by Frannie Crystal"; admin view on @helenhearthealer.
- **SourcingXpro:** Fran wrote the captions, generated video topics and edited the videos.
- **Starrz PR:** Fran made the graphics and wrote the captions; headshots were supplied by the client.
- **Lighthouse Declaration:** Fran posted regularly, selecting from a pool of quotes contributed by volunteers. She did not claim the template design. Shown by name, with the note that views belong to those quoted.
- **Dr Sam White:** Fran made the graphics and wrote the captions.
- **Tools & skills (confirmed by Fran):** Canva, CapCut, HeyGen, OpusClip; Instagram, Facebook, LinkedIn, Pinterest, YouTube; content creation, video editing, content repurposing, social media scheduling.
- **Process (confirmed by Fran):** general social media workflow: plan, create, write, schedule and publish, repurpose.

## Decisions

- Clients are described, not named, on the public site: wellness & leadership coach (personal brand + leadership company), B2B sourcing company, functional medicine practice, advocacy campaign, PR & events agency. Screenshots still show brand handles; Fran accepted this. Public image filenames are neutral (`scripts/build_site.py`).

- No analytics, insights or performance numbers on the portfolio. Fran does not want to reveal client data. Crop out "View insights", "Boost post" and similar admin UI from screenshots.
- No dates anywhere on the portfolio: not in captions, and Facebook date headers are cropped off screenshots.

## Still open

- "Published by cacao calling" on a Heart Healer Facebook post: another publisher or a tool?
- Design direction: chosen. Version 3, Split story (`drafts/v3-split.html`).

## Systems portfolio (/systems/)

Confirmed from Fran's brief for this site: ~15 years corporate experience; background in digital marketing implementation, CRM workflows, funnel building, email marketing, website management, business operations. Tools worked with or used in project environment: GoHighLevel, HubSpot, Kajabi, Kit, Kartra, Wix, Vercel, GitHub, Neon, Claude Code, Zoom.
- Full tools & tech stack confirmed from Fran's stack graphic (see TOOLS in src/systems/data/make_page.py).

Decisions for the systems site:
- Fran built all six projects end to end: pages, assessment/booking steps, CRM fields and tags, email automation, calendar connections, QA and maintenance (confirmed).
- Clients described, not named; no links to client sites; no per-project tools (the Tools page covers them).

Still open for the systems site:
- The six reference sites (Courage Type, The Four Worlds, Zipline assessment, Riana Malia ELI, Powerhouse Profile, SalesClosers) could not be loaded from the build environment (DNS blocked). Nothing about them is described beyond Fran's own brief. 
- Hands-on depth per tool (not shown until confirmed).

## Systems site build types (confirmed)

- Build types: Assessment, Masterclass, Book a call, Application, Lead gathering (enrollment blueprint removed).
- Client builds from supplied screenshots: 5 assessment funnels (non-profit board effectiveness, courage profile, relationship pattern diagnostic, four-worlds inner map, emotional pattern profile) and 1 book-a-call funnel (fractional sales talent agency). Built end to end by Fran.
- Masterclass, application and lead gathering: no client samples supplied yet; shown as blueprints with "examples on request".
- Supplied screenshots are low resolution (300-600px wide); sharper top-of-page screenshots would improve the previews.

## Systems site: one page (current)

- Single page: hero, six client builds (not categorised), five funnel flow charts (assessment, masterclass, book a call, application, lead gathering), services, tools, about, email contact. No contact form.
