# Maryland Eagles Eyes — continuation

The user authorized building this welcome page, creating/pushing a GitHub repo,
deploying to Vercel and configuring 122eagles.com. Preserve the simple welcome
scope, current bridge photograph and design. Read before continuing.

## Site and domain — complete

## Editorial focus — November 4, 2026

- New direction: highlight challenges facing Marylanders and practical solutions
  anyone can take up to help solve them. This includes challenges faced by
  businesses, students, workers juggling multiple jobs, and struggling founders;
  these are examples, not limits on coverage.
- GitHub repository description updated and verified:
  “Highlighting challenges facing Marylanders and practical solutions anyone can
  take up to help solve them.”
- Homepage and About copy now implement this direction (publication update below).
  Preserve the existing design and simple page scope.

## Existing site and domain details

- Site: https://122eagles.com/ ; Vercel alias https://122eagles.vercel.app/.
- Exact heading: Welcome to Maryland Eagles Eyes.
- Public-domain photograph of Maryland's Chesapeake Bay Bridge, Carol M.
  Highsmith / Library of Congress. See public/assets/PHOTO-CREDIT.md. Responsive WebP
  assets and self-hosted Lora/Instrument Sans fonts; no tracking or packages.
  motion.js is a tiny first-party deferred script that starts the camera after
  the photo loads and decodes; include it in deployment files. CSP script-src
  permits self only. Page content remains visible if the script cannot run.
- User requested motion: staggered welcome/Maryland/Eagles Eyes entrance plus
  gentle mirrored wing movement and slight lift on the eagle every 10 seconds.
  Most of the cycle rests. All animation uses opacity/transform and is disabled
  for reduced motion. User subsequently requested cinematic bridge motion: the
  photograph now has a clearly visible 4.5-second opening push-in followed by
  a wider 20-second alternating diagonal pan/zoom. The opening starts when the
  photo appears, including slow mobile downloads. The bridge structure does not
  deform, text stays steady, and no image edge is exposed.
- Mobile source now offers 1x/2x assets: high-density phones get the 1920px photo
  while standard-density phones retain the smaller 960px image. Chromium mobile
  profiles (iPhone SE, iPhone 13, Pixel 7) pass touch/DPR, complete camera cycle,
  rotation and viewport-resize continuity, edge coverage, playback and reduced
  motion checks. Delayed-image test confirms the camera waits for decode.
  Opening-frame checks at 320/390/844 landscape/1440/2560 confirm a visible
  first-second push-in and stable text.
- Native iOS hardware is unavailable. WebKit download succeeded but this host
  lacks its system libraries, so these are Chromium mobile emulations, not a
  claim of real-device Safari testing.
- Motion checks verified staggered progress, full final text visibility and
  mirrored wing transforms. Seven responsive/reduced-motion layouts passed:
  320,390,600,601,844 short landscape,1440,2560px. No overflow, fonts/photo load,
  no external runtime requests. Social preview matches the current design.
- Apex A: 216.198.79.1 and 64.29.17.1. www CNAME:
  6320fd3e556bc659.vercel-dns-017.com. Namecheap BasicDNS nameservers unchanged.
- Both Vercel get_domain_config results: misconfigured false.
- HTTPS apex returns HTTP200; www returns HTTP308 to https://122eagles.com/.
  Verified using normal TLS curl, and actual custom-domain browser checks at
  390/1440px (page, photo, fonts, no overflow, reduced motion).
- Five email-forwarding MX records and SPF/TXT match the pre-change public
  baseline. /tmp/122eagles-dns-before.json and /tmp/122eagles-mail-after.json.

- Current mobile cinematic update: commit c9236e1, deployment
  dpl_DX1dse1hKp4HADzXebS4qjb1wb4h is READY. Actual https://122eagles.com checks
  passed all three Chromium mobile profiles, including high-density image
  selection, full camera cycle, touch, rotation/resize continuity and reduced
  motion. Standard-density phone still chooses the smaller asset. Public
  motion.js exactly matches source and its first-party CSP permits execution.

## Hosting

- Vercel project 122eagles / prj_Wmor3GXuz4VGB2Dd77qDhEQdRwY9.
- Team toluadetuyis-projects / team_1HRMSafo3kjx8ErMiKg6Rlww.
- Static HTML/CSS/JS, framework Other/null, no install/build commands, repo root,
  output directory public/.
- Text/eagle animation deployment dpl_JB3mRJ5igcWqcbumNYysnrhVo4ZR was READY.
  Actual apex checks passed normal and reduced motion; www HTTPS redirect passed.
  Prior cinematic deployment dpl_AMM8EUYzNw5VoVs6Lg4tg4Un6yyW is READY
  (site commit d90188f). Live mobile/desktop checks verify actual camera movement
  and reduced-motion behaviour. Local checks at 320/390/1440/2560 verify all
  pan/zoom positions cover the frame and the heading geometry remains fixed.
- Standard Vercel protection prod_deployment_urls_and_all_previews; production
  aliases/custom domains public, previews/deployment URLs protected.

## GitHub and automatic deployment — complete

- Private repository: https://github.com/Threadigit/122eagles, id1445253846.
  Local origin points to this repository; production branch main.
- Existing Vercel project prj_Wmor3GXuz4VGB2Dd77qDhEQdRwY9 in team
  toluadetuyis-projects is permanently linked to GitHub Threadigit/122eagles.
- Website files live in public/. Root vercel.json sets outputDirectory public;
  no install/build command is needed. Runtime URLs and rendered design remain
  unchanged. Internal continuation notes are not published (HTTP404 verified).
- Automatic deployment was proven by git push alone, without create_deployment:
  verification commit d4144ad021b425e5384259b73542556d2a16a55d triggered
  dpl_5HqKCEfUPH5NCREYPfAcsozForLw, source git, branch main, target production,
  state READY. Its GitHub metadata matched the exact SHA/org/repo, and aliases
  included 122eagles.com and www.122eagles.com.
- Live HTTPS HTML and motion.js exactly matched the pushed source, and www
  returned308 to the apex. Mobile cinematic checks passed after the Git layout
  migration; all runtime files had moved byte-for-byte.
- Future work: edit public/ and git push origin main. Vercel builds and deploys
  automatically. No manual upload, GitHub Actions secrets or extra project is
  required. All requested GitHub/domain/deployment setup is complete.

## Browser history / avoid duplicate work

- Default TinyFish profile prof_f047cdc863044f54 eventually reached authenticated
  Namecheap after the user's renewed sign-in confirmation. It is the profile to
  use for any later authorized changes; signed_in_sites metadata was empty even
  when a run successfully authenticated, so do not treat it as definitive.
- Dedicated Namecheap profile prof_91ba5a2dbbf740e2 never supplied a session.
- Run ba1b581f-fb1d-4444-8e05-cf39b9a2947b saved the first apex A, removed parking,
  then ended with a form-validation issue on an optional second A.
- Focused www run 61c29eac-73ac-4fc6-8f88-7702dc2b25a3 completed blocked by a
  Cloudflare check. It is NOT active. The user then completed the Namecheap DNS
  updates; subsequent Vercel, HTTP, redirect and mail checks all passed.
- No DNS work remains. Do not repeat the old sign-in/setup loops.

Local preview: python3 -m http.server 8012 --directory public. No registrar transfer, nameserver
migration or purchase is needed. Do not change other projects or records.

## Newsletter copy and on-site signup — complete

User requested “Maryland, made clear.” plus the policies/projects/programs copy,
“Five minutes. Free. Every week.” and “Open your eyes” as the subscription action.
They supplied https://buttondown.com/eagles/ and want readers to sign up on the
website rather than navigate to that hosted newsletter page.

Branch feat/maryland-newsletter-signup / PR https://github.com/Threadigit/122eagles/pull/1
adds the exact copy under the existing animated publication name, tighter
responsive heading spacing, updated metadata, and an active warm-white CTA.
It opens a branded native dialog; subscribe.js lazily loads Buttondown's official
https://buttondown.com/eagles?as_embed=true form inside it. Readers stay on our
URL, while Buttondown owns validation, CAPTCHA and confirmation. No API key,
server-side credential, custom subscriber store or paid integration is needed.
No fake success is shown by our page. The visible close button remains available;
Escape works while focus is in the parent document (cross-origin frame key events
do not bubble to the parent). Closing restores CTA focus and resumes the camera.

Only frame-src https://buttondown.com was added to the CSP; script-src remains
self and parent form-action remains none. Provider scripts run under its own
frame policy and do not load on the landing page before a reader opens signup.
A no-script embedded-form fallback is included.

For the public signup flow, provider docs recommend an iframe or web component
when staying on-site, and prohibit JavaScript fetch to embed-subscribe. This
integration uses the official iframe; a separate private API integration would
require server-side credentials and was unnecessary for the requested flow. A trial native form
submission targeting a frame did not work and was removed. An empty submission
was used for that check; no actual email recipient or subscriber was created.
Final QA only renders the live provider form and checks invalid/valid syntax
without submitting an address or sending mail.

Tests: tests/subscription-browser.py covers 320/390/844 landscape/1440px using a
provider-frame fixture: lazy load, native email validity, same-page display,
modal close/focus, cached reopen, reload and reduced motion. Optional live mode
reads the actual Buttondown form without POST. Test URL env EAGLES_TEST_URL;
EAGLES_LIVE_FORM=1 enables read-only live form check. Actual CSP local preview is
/tmp/eagles-csp-server.py at port8013 (reads vercel.json headers).

PR #1 is merged at fd0fab818dc9b399dbdc5184479f42f5a647ff99 and attached to
this task. Git-triggered production deployment dpl_DdLPHA5mTK7RsJ7QaAH6iUQFwN7x
is READY. Live tests passed at 320/390/844 landscape/1440, including the actual
Buttondown form render and validity checks with no POST or test subscriber.
Production HTML exactly matched the merged source. Copy, social preview and
working on-site signup are now live at https://122eagles.com/.

## Signup confirmation and Maryland SEO — November 4, 2026

Branch fix/signup-branding-maryland-seo fixes the provider's confirmation being
clipped inside the original 230px iframe. A responsive 360–440px frame and wider
560px maximum dialog leave room for its full message and both Gmail/Got it
actions. On short screens the outer dialog scrolls; its close toolbar remains
sticky. Provider state is preserved across close/reopen. No automatic dismissal
was added. The user chose to update Buttondown branding themselves and received
Settings → Design instructions with `--color-action: #172b36`. Read-only live
provider checks now observe matching navy buttons; no account settings, paid
plans or email configuration were changed by this agent.

SEO: Maryland newsletter title/description, full OG/Twitter metadata, Organization,
WebSite, WebPage and Periodical JSON-LD, plus an indexable /about page describing
policies/projects/programs and the weekly free offer. Homepage footer links to
About; its signup link opens /#subscribe. Sitemap lists both canonical pages with
lastmod. No invented reporting, local addresses, reviews or keyword city pages.
Original hero, typography and camera remain. Search Console ownership verification
and sitemap submission still require the owner's Google account; no rankings or
indexing are promised.

Checks: 320/390/844 landscape/1440px signup fixture flow passes. Actual Buttondown
form validation and confirmation preview pass at those widths without posting a
subscription: full message above actions, navy button, Got it dismissal and sticky
parent close. Provider analytics POST /cdn-cgi/rum is excluded from the no-signup
POST assertion. CSP browser checks pass both pages, no JS/console errors or
horizontal overflow, JSON-LD present and About signup deep link works. Static SEO
checks validate canonicals, metadata, structured JSON, internal links and sitemap.

PR #2 https://github.com/Threadigit/122eagles/pull/2 is merged at
2a0291d7b676b84017bb08dcc38992a0e4b1c66e. Automatic Git production deployment
dpl_EwYx5ih99Eebgro9FX9ru16Z1dk3 is READY. Public HTTPS homepage, About, CSS,
subscribe.js, sitemap and robots match merged source byte-for-byte. Live signup
fixture and actual provider form/confirmation checks pass at all four viewport
sizes, including Gmail actions, navy colour and sticky closing; no subscription
or confirmation email was sent. All implementation work for this request is
published. Owner-account Search Console verification/submission remains pending.

## Publication direction — November 4, 2026

Homepage and About now position Maryland Eagles Eyes as a publication about local
challenges and practical solutions. The homepage retains the bridge, motion and
welcome design. About introduces The Maryland Brief: people, obstacle, possible
solutions, who can act, and dated follow-ups; it includes eight everyday-life
coverage areas. EDITORIAL_DIRECTION.md contains the story template, launch leads,
evidence standards and release workflow. No unreported stories are presented as
finished work, and no nonfunctional contact form was added.

Signup remains the existing Buttondown integration, now offering free updates
when stories/follow-ups publish rather than a weekly newsletter. Titles, metadata,
structured data and social preview follow the publication positioning. Git pushes
do not send subscriber mail: the publisher must send the corresponding editorial
update in Buttondown. No campaign sent or email automation configured.

Validation: SEO/internal-link/JSON-LD checks pass. Chromium checks at
320/390/844 landscape/1440px pass for both layouts, About signup deep link,
lazy signup, validation, modal close/focus, reopen/reload and reduced motion.
Screenshots reviewed on mobile and social preview. Commit 05ed2d3 pushed to main;
Git-triggered production deployment dpl_DVVHoe5CBno3pbGhvpvLREvKNXSL is READY.
Live homepage, About, CSS and social preview match committed source byte-for-byte.
Live layout and About deep-link checks pass at all four widths. Live signup
regression checks pass; actual Buttondown form renders and validates email syntax.
No subscription or campaign was sent. Production verified at https://122eagles.com/.
This verification record is a local continuation-note update after publication.

## Domain migration and editorial refinement — November 4, 2026

User purchased mdeagles.com at Namecheap and authorized moving the site there.
Vercel apex and www project domains added and ownership verified. www redirects
to apex (308). Required DNS: @ A 216.198.79.1 and 64.29.17.1; www CNAME
6320fd3e556bc659.vercel-dns-017.com. Nameservers stay at Namecheap BasicDNS.
Baseline: apex parking IP 192.64.119.243, www parking CNAME; five eforward MX
records and TXT v=spf1 include:spf.efwd.registrar-servers.com ~all. Preserve mail.
TinyFish DNS run ce32d023-e427-40ef-b848-e5390ad94b2d uses the prior default
profile; completed with no DNS changes because the saved session expired.
User completed DNS manually. No further Namecheap browser work is needed.

Masthead changes from 122eagles to MD Eagles; publication title remains Maryland
Eagles Eyes. About rewritten as restrained prose with no card, numbered pitch,
category grid or em dashes. Existing bridge and motion preserved. Canonical,
structured-data, sitemap, robots and social URLs move to mdeagles.com.
Both page layouts and About signup navigation pass at 320/390/844/1440px.
SEO and signup regression checks pass. Public DNS and Vercel config confirm both
new domains are correctly configured; five MX records and SPF remain unchanged.
Issued auto-renewing TLS certificate cert_F9fVkMZfawpE2vGK2ksSsCVg for apex/www.
HTTPS apex returns 200 and www redirects 308 to apex. Old-host redirects are
included in vercel.json. Commit 9180376 pushed to main; Git deployment
 dpl_FZSuWRFF8RHhQ5SCCdLAjKz3NbLi is READY in production.
Live files match source: homepage, About, CSS, robots, sitemap and social image.
Old apex/www and new www redirects preserve /about and query strings, ending at
https://mdeagles.com with HTTP200. Both page layouts and About signup navigation
pass at 320/390/844 landscape/1440px; signup regression checks pass at all widths.
The primary site is now https://mdeagles.com/; 122eagles.com is a redirect.
Repository and Vercel project identifiers remain 122eagles to preserve integration.
No further DNS setup is needed. This verification record is retained locally.

## Problem-led discovery — November 4, 2026

User explicitly expanded the welcome-page scope into a useful searchable Maryland
publication, prioritizing finding help over subscribing. This supersedes earlier
welcome-only scope; preserve bridge photography, type and restrained design.

Homepage now provides search, eight need-based tiles and three editorial starter
guide links. Subscription is a secondary section below content. `/guides` supports
keyword/topic filtering, common synonyms, shareable query URLs, reset, no-results
and full no-JavaScript browsing. Eight crawlable guides live under `/guides/`.
Each includes audience, geographic scope, provider action, suggested steps, a
question to ask, limitations, review date, source and related guides.

Content sources: Maryland DHS OHEP, DHCD renter resources, Labor job centers,
Maryland Family Network LOCATE, Maryland SBDC, USM essential resources, Maryland
Health Connection, and Maryland Access Point. Sources reviewed November 4, 2026.
These are introductory resource guides, not original reporting or guarantees of
assistance. USM scope is explicit; no invented county-level filter or availability.
MHC source readable via web tool but direct browser receives provider anti-bot 403;
its verified consumer phone route is included as an alternative. Other provider
links return 200 in curl or Chrome (USM requires Chrome's certificate trust).

Data: content/guides.json. Run scripts/build-guides.py to regenerate directory,
guide HTML and sitemap. Homepage curated content is separately maintained.
README and EDITORIAL_DIRECTION explain maintenance and future Brief integration.
CSP form-action now allows self for local GET search; external subscription still
uses the existing isolated Buttondown iframe. No external search service, subscriber
send, analytics or server-side store added.

Local discovery tests pass at 320/390/844 landscape/1440px: search submission under
CSP, terms, topic/reset/reload, empty state, provider actions, no-JS, all guide
routes, no overflow/errors. Signup regression and reduced motion pass after
removing residual headline animation from the new hero in reduced-motion mode.
SEO/sitemap/internal links pass; homepage, directory and guide screenshots reviewed.
Final natural-language queries and reduced-motion checks pass across all four
viewports. Prefix/word search avoids matching rent inside parent. Production
push complete: e3d19c8 on main, production deployment
 dpl_C5DLw1R1pkKUbDdLTAdUbD2vVkya READY. Live files match the committed homepage,
About, directory, discovery CSS/JS, sitemap and social preview. Discovery journeys
pass on https://mdeagles.com at all four widths, including all eight guide routes
and no-JavaScript browsing. Signup regression and actual Buttondown form validation
pass without submission. Old-domain /guides?topic=work redirects correctly.
The new discovery experience is live. This final verification note remains local.

## Builder-first correction — November 5, 2026

User rejected the prior visual design and explicitly superseded preserving it.
Core is now documented Maryland problems and solutions residents can take up.
Rebuilt with plain GOV.UK-inspired service-directory conventions: white background,
Arial, underlined links, simple rows; no photo hero, animation or decorative cards.
`/problems` is the first navigation item and homepage primary action. Three sourced
briefs cover Baltimore child care/work, Maryland employer cash flow, and skilled
immigrant career barriers. Proposals are explicitly untested; no implied partners.
Each includes evidence limits, first steps, possible collaborators, measures,
existing services and a real downloadable project worksheet. Source review date
November 5, 2026. Resource guides and lazy Buttondown subscription remain secondary.
Generators: build-problems.py then build-guides.py (which rebuilds full sitemap).
Pending: finish browser QA, push, verify production.

Local QA complete: problem search/filter/reload, no-JS browsing, all brief routes,
worksheet download contents, resource search and all eight guide routes pass.
Mobile/desktop layouts at 320/390/844/1440px have no overflow. Screenshots reviewed.
Signup regression passes all four widths, including lazy load, validation,
close/focus, reopening and reload. Dialog scroll now resets on reopening.
SEO, sitemap and internal links pass. No email submitted or campaign sent.

Published commit ead448f34ececa66173bf8f22273ce9bf0f145a9; Git-triggered production
 deployment dpl_E2LCZPY5ZCBAoMDgnygvDyGArwTz is READY. Production homepage, About,
CSS, problem directory, search script and sitemap match tested source exactly.
Live problem journeys pass at all four widths, including filters, query reload,
brief navigation and downloaded worksheet content. Live signup regression passes
at all four widths without submission. Test now waits for deferred search script
navigation completion before typing. Final verification notes retained locally.

## Editorial identity refinement — November 5, 2026

User clarified that usability references should inform the structure, while MD
Eagles retains its own modern visual identity. Replaced the government-like
black/green/Arial presentation with warm paper, deep blue, copper, Lora headlines
and Instrument Sans text. Eagle masthead restored. Homepage now has an editorial
split composition with restrained Chesapeake imagery, simple problem rows and a
secondary resource column. Subscription remains secondary. Shared styles carry
through About, directories, problem briefs and resource guides. No animations.
Source generator updated; responsive image sources and original photo credit kept.
Local browser checks pass at 320/390/844/1440: problem search/filter/downloads,
resource journeys, no-JS browsing, signup validation/reopen/reload/focus, overflow
and reduced motion. Homepage screenshots reviewed at mobile and desktop widths.
SEO/sitemap/internal-link checks pass. Publishing through the existing Git workflow.

Published 67d8c30857db115b612ddbd6ccb9a957182a4ee0 to main. Production deployment
 dpl_5jVrny2oZQGufeMcnfeGYU6sU2Tq READY. Live homepage, About, problem directory
and stylesheet match source exactly. Live problem search, filters, navigation,
worksheet downloads and layout pass at 320/390/844/1440px. Final record kept locally.

## Senior-editor redesign: cinematic bridge, cleaner system — November 5, 2026

User asked for the site to stop looking vibecoded, with the problem collection as
the core and resource guides for everyday residents, plus the Bay Bridge in a
cinematic mode that works on mobile and web, with the eagle as the logo. This
supersedes the older "preserve the existing design" notes above.

Published: commit c4789e9 pushed to main; Vercel Git deployment is live at
https://mdeagles.com (style.css matches source byte-for-byte; cinema.js, film
photo and brief pages return 200). Contents:
- Homepage opens with a graded, full-bleed Bay Bridge film: slow diagonal camera
  drift plus a 7s push-in, eagle mark drawing itself and flapping once every 10s.
  CSS transform/opacity only; cinema.js starts it after decode and pauses it
  off screen; reduced motion shows a still. Art-directed for portrait phones
  (horizontal pan) and landscape (vertical pan). Edge coverage checked in the
  browser pane across the whole camera cycle at 390x844, 1440x900 and 844x390
  (no exposed edge).
- Photograph graded in scripts/grade-photo.py (master in content/source/); new
  assets bay-bridge-film-960/1920.webp. Social card regenerated by
  scripts/make-social-card.py; og:image and twitter tags added to every page.
- Problem collection is now a numbered ledger (place, topic, evidence, status)
  on the homepage and /problems; briefs open with a fact strip. Resource guides
  have their own homepage band with search and all eight guides. Slogan copy
  removed. Nav is "Problem collection / Resource guides / About".
- Build consolidated: scripts/build.py + scripts/layout.py replace the circular
  build-problems.py/build-guides.py. style.css rewritten as one readable file;
  discovery.css and motion.js removed. scripts/serve.py mirrors vercel.json
  (clean URLs, CSP); .claude/launch.json points the preview at it.
- Checked in the browser pane: homepage at 390/1440, brief page at 390, guide page
  at 1440, problem search/filter/empty/clear, signup dialog opens, no CSP errors.
  tests/seo.py passes.

Not done / not verified: Python Playwright is not installed here (pypi blocked in
the sandbox), so tests/*-browser.py were updated for the new selectors and link
names but NOT run. Real-device Safari untested. Pending: run those tests where
Playwright is available and check the live homepage on a real phone.

## Second overhaul: premium night system, two-fold platform — November 5, 2026

User rejected the first redesign ("still terrible") and asked for a drastic overhaul:
problem collection must come with possible solutions, and the site must tell visitors
they can also find resource guides to problems already solved, by county or by life
area. Built locally; NOT yet committed or pushed (live site still shows c4789e9).

- New dark cinematic system (night navy, gold accent, ivory reading sections); Instrument
  Sans display type; fixed header that fades in a dark bar on scroll (CSS scroll timeline,
  solid fallback); scroll-reveal via CSS view timelines (progressive enhancement).
- Homepage: full-height bridge film, headline "Fix what’s missing. Find what already
  works.", two "doors" (Problem collection / Resource guides), problem cases with their
  possible solutions inline, a resource section with county picker, life-area chips and
  all eight guides, then email signup and a richer footer.
- Inner pages open with a dark band using a still crop of the graded bridge. Briefs show a
  fact strip and a dark "Possible solutions to test" panel of cards. /guides gains a
  county selector plus search and need filters; county shows an "ask which office serves
  X County" note on local guides and never filters (no county data is invented).
- Tests updated for new selectors and wording (door link, "Search the collection", county
  note); NOT run (Playwright unavailable here). Verified in the browser pane: film edge
  coverage over the full camera cycle at 390/1440/844x390, no horizontal overflow at 320
  on all page types, county note and filters work, tests/seo.py passes.

## Third redesign: golden hour in your neighborhood — November 5, 2026

User said the structure was right but the UI/UX still was not premium, and asked for a
clock by time zone, a welcoming neighborly greeting, premium navigation and movement,
and to research first. Research and decisions are in DESIGN_DIRECTION.md. With the
user's permission this session downloaded Instrument Serif (OFL, via Fontsource and the
Instrument GitHub repo) and four public-domain Highsmith photos from loc.gov
(credits in public/assets/PHOTO-CREDIT.md). Published to main (commit message: Third redesign: golden hour in your neighborhood).

- Welcome: greeting by visitor's local hour (+ chosen county), Maryland clock, visitor's
  own time when it differs, sunrise/sunset from NOAA equations (matches published
  Baltimore Nov 5, 2026: 6:37 AM / 5:02 PM), hero sky tinted by phase. ?demo= on localhost.
- Navigation: floating island with sliding highlight, hides on scroll down / returns on
  scroll up, full-screen mobile menu (focus trap, Esc, inert page), scroll progress hairline,
  cross-document view transitions (Chrome/Safari; progressive enhancement).
- Aesthetics: serif display type, parchment/navy rhythm, county tile map of the 24
  jurisdictions linking to /guides?county=, photo collage and bands, grain, stacked sticky
  problem cases on wide screens, pointer light on doors, masked line reveals.
- Removed Lora and old social images; scripts: prepare-photos.py, grade-photo.py (daylight
  base), build.py/layout.py; new tests/welcome-browser.py.
- Verified in the browser pane: all five sky phases + DST (July sunrise 5:44 AM, sunset
  8:35 PM), greeting and county memory (home to guides), mobile menu open state, no
  horizontal overflow at 390/320, hero fits one viewport at 1440x900, film edge coverage
  (previous check). Playwright tests NOT run (not installed here); real-device Safari untested.

## Logo animation, county detection, coral accent, polish audit — November 5, 2026

Published to main (commit: Animate the nav logo, detect county on-device, coral accent, polish).
- Removed the floating eagle from the hero; the nav logo mark itself now animates (draws on once
  on the homepage, wings beat every 10s, extra beat on hover).
- County auto-detect: "Use my location" (hero clock panel, tile map, /guides) plus silent detection when
  location is already allowed. On-device point-in-polygon against 26 KB of simplified Census shapes;
  no coordinates leave the browser. Verified: 24/24 sample towns map to the right county, six out-of-state
  points return none, success/outside/denied flows update greeting, dropdown and tile map.
- (Superseded: coral was rejected by the user.) Accent was changed from muted amber to coral;
  one token set at the top of style.css (--hot, --hot-rgb, --hot-hover, --hot-ink). Amber was the
  assistant's own choice; user asked for something that pops.
- Audit: non-breaking hyphen (missing from both fonts) replaced; county names use typographic
  apostrophes; photo credits align to the content edge; county tile text sized to fit. Measured left/right
  edges of every major block at 1440 (all on the grid), and no clipped text or horizontal overflow
  at 1440/1024/390 on the home, problems, brief, guides and about pages. Surface polish added
  (inner highlights, glows, shadows). Playwright tests (incl. new detection test) NOT run here.

## Colour, italics and a real Maryland map — November 5, 2026 (published to main)

User rejected the coral ("terrible") and asked for research, a view on italics, and to turn the
county tile region into a map of Maryland. Research is summarized in DESIGN_DIRECTION.md.
- Accent is now Chesapeake sea-glass teal: --hot #4fdcc4, --hot-ink #0a6b5e (compared on the live
  page against flag gold, coral and sage; sage was washed out, gold/coral clashed with the navy).
  New navy/teal favicon (assets/favicon.svg); social card regenerated. eagle.svg is untouched.
- Italics limited to one headline phrase per section (ink colour, not accent), the greeting, hero
  second line, map Bay label and quotations; numerals, markers, footer tagline and menu are roman.
- The tile map is replaced by a real SVG map built at build time from md-counties.json: cream land on
  sea-glass water, county labels where they fit, hover linked to the county list, selected county
  in teal with a pulsing pin, counties settle in on first view. The SVG is aria-hidden; the list of 24
  links under it is the keyboard/screen-reader path. On phones the intro sits above the map and the
  list is two columns. Guides page: the location button moved out of the filter row so fields align.
- Verified in the browser pane at 1440, 1024 (earlier audit) and 390: map renders and reveals, list
  hover highlights the map county, no horizontal overflow. Playwright tests not run.

## Maryland brand colors and no italics — November 5, 2026 (published to main)

User asked to adopt Maryland government colors and minimize italics. State brand colors (digital.maryland.gov brand
sheet and Health Dept logo standards, via search summaries; PDFs 404 for fetch, so unverified against the
originals; flag Pantone sheet is slightly different: PMS 201 red, PMS 124 gold): red #c8122c, gold #ffc838,
near-black #231f20, white.
- Tokens: --hot = gold (dark-surface highlight), --hot-ink/--red = red (light-surface highlight and every button),
  dark surfaces = near-black (#231f20, cards #2d2829, footer #171415), inks warm near-black. Teal removed everywhere
  (favicon is now near-black + gold; social card regenerated; worksheet link colour red). Map: white land on warm paper,
  selected county gold with a pin, hover near-black.
- Italics: none left except the quoted question on guide pages; headline emphasis is tonal (muted second clause);
  hero second line and greeting are gold roman.
- Added independence statements (footer and About: not affiliated with or endorsed by the State of Maryland; colors are
  a tribute to the flag) because the palette looks official. No state seal or logo used.
- Checked in the pane: hero, welcome, collection, map, subscribe band and footer at 1440; 19 sampled text colours all
  >= 4.5:1; zero italic elements on the homepage. Mobile and 1024 not re-screenshotted after the recolour (layout
  unchanged). Playwright tests not run.

Red refinement (published to main): user said "the red looks off". Flat #c8122c with a red glow looked
muddy on the warm photo and near-black surfaces. Buttons and the island CTA now use a lit gradient fill
(#e0213b to #ae0f25, brand red in the middle), an inset top highlight and a neutral shadow instead of a red halo;
small red text on light surfaces uses a slightly deeper #b50f28. Brand red #c8122c itself is unchanged.

## Restraint like maryland.gov, and no red — November 5, 2026 (published to main)

User asked to check how maryland.gov combines the brand colours, then said not to use red at all.
Findings from maryland.gov: white canvas, near-black text (#1b1b1b), grey hairlines, USWDS blue links (#005ea2), serif display
headings, dark footer; the brand red and gold appear only in the flag logo mark (my scan found no brand colours in its UI).
- Removed red everywhere: buttons are near-black on light surfaces and white on dark (island CTA is a white pill), labels are
  grey, light-surface accents are near-black, hover shows a gold underline, focus ring is near-black on light and gold on dark,
  the quote bar is gold, Word worksheet links are near-black. Scan of computed styles on the homepage: zero reddish colours.
- Tried and removed a gold/black stripe ribbon on the footer (looked like road tape).
- Gold remains the only brand highlight on dark surfaces. Not re-screenshotted on mobile or 1024; Playwright tests not run.

## Favicon set — November 5, 2026 (published to main)

The favicon was a single thin-stroked SVG: hard to read at 16 px and unsupported by Safari and some other clients. Now
scripts/make-favicons.py draws the eagle bolder (gold on near-black) and writes favicon.ico (16/32/48), assets/favicon.svg,
apple-touch-icon.png (180), icon-192/512.png; every page links ICO, SVG, Apple icon and site.webmanifest, and the
Organization logo in JSON-LD is icon-512.png. assets/eagle.svg is untouched. Browsers cache favicons hard, so a hard refresh
or reopening the tab may be needed to see the change.

## Fonts switched away from the AI-default pairing — November 5, 2026 (published to main)

User asked to confirm the fonts are not the popular vibe-coded ones, and to switch to nestpay.co's if they are.
Research: Instrument Serif is widely cited as a default of AI-generated/vibe-coded sites (and Instrument Serif + Instrument Sans
is a common pairing), so yes, ours was a tell. The assistant had wrongly called it "distinctive" earlier.
nestpay.co (inspected live): headings Schibsted Grotesk 600/700, body and UI Hanken Grotesk 400/500, both Google Fonts via next/font.
- Downloaded (with the user's go-ahead to switch) the Fontsource variable latin builds: schibsted-grotesk.woff2 (46,752 B),
  hanken-grotesk.woff2 (34,704 B) plus their OFL licences. Both cover every character the site uses (checked with fontTools).
- Removed Instrument Sans/Serif (and the italic face) and their licences. --serif/--sans are now --display/--text. No italics remain
  anywhere (the quoted question is medium-weight roman with a gold bar). Display is semibold with tighter tracking; the whole type
  scale was retuned because grotesk is wider than the old serif. Social card regenerated with the new fonts (variable axis pinned).
- Checked: hero fits one viewport at 1440x900, no horizontal overflow or clipped text at 390 on home/problems/brief/guides/about,
  fixed the band photo credit starting at the screen edge on phones. Not re-screenshotted at 1024; Playwright tests not run.

## Favicon cache fix — November 5, 2026 (published to main)

User saw a green (teal) favicon. All live icon files are gold (verified byte-for-byte and by sampled pixel colour); the teal one was
live only briefly (ffa81c2) and is cached by the browser under the same URLs. Icon links and the manifest icons now carry ?v=2
(ICON_VERSION in scripts/layout.py) so browsers fetch fresh files. A browser that cached the old icon may still need its cache cleared
or the site re-bookmarked once; Safari and iOS home-screen icons are the stickiest.

## Fonts: america.gov's structure with free lookalikes — November 5, 2026 (published to main)

User asked to use the font from america.gov. Inspected live: headlines (h1, nav) use "Rhymes Text/Display" (Maxitype, commercial) and
text/h2/h3 use "Helvetica Now Text/Display" (Monotype, commercial), served as woff2 from america.gov/_astro. Those files are licensed to
that site, so they were NOT copied. User chose "free lookalikes": Newsreader (OFL, variable wght+opsz, 132,000 B woff2, from Fontsource)
for page titles, big statements, numerals and the wordmark; Hanken Grotesk (already installed) at 500 for smaller headings and 400 for text.
Schibsted Grotesk and its licence removed. Social card regenerated. No italics. Option to buy the real fonts remains (swap the two woff2
files). Checked: hero fits at 1440x900 and reads well on a phone; no overflow or clipped text at 390 on home/problems/brief/guides/about;
glyph coverage of both fonts complete. Not re-checked at 1024; Playwright tests not run.

## Mobile map fix — November 5, 2026 (published to main)

On phones the map was a 320 px wide speck (Howard 32x21 px, names hidden). Now below 760 px the SVG is 900 px wide inside a swipeable
wrapper (edge fade, names visible, starts centred on the chosen county, hint "Swipe the map, then tap a county"); on touch devices the
first tap previews a county (highlight + "See local help in X County" button) instead of leaving the page. Desktop unchanged. Verified in the
390 px emulation: Howard is now 89x59 px, tap preview works. Not verified on a real phone; Playwright tests not run.

STILL TO DO (requested, not started): end-to-end walkthrough of the platform, trimming over-long UI copy (hero lead, doors, hello, About,
map intro, directory notes), and final polish (branded 404 page, print styles for guides/briefs, accessibility pass).

## Walkthrough, copy trim and final polish — November 5, 2026 (published to main)

- Text audit of every page (visible words): home 917 to about 800, problems 499 to 474, guides 432 to 406, About 333 to 285. Cut UI copy on the
  hero lead, doors, "welcome", collection and resources intros, map caption, updates, problems/guides leads and notes, brief solutions note,
  worksheet note and About. Homepage cases now show only the first sentence of each possible solution (full text is on the brief and /problems).
  Guide and brief content (from content/*.json) was left as written.
- New branded 404 page (public/404.html, noindex, excluded from the sitemap; tests/seo.py skips it).
- Print styles: guides, briefs and worksheets print without navigation, photos or forms, external link URLs are printed after the link text.
- Accessibility audit on home, problems, a brief, guides and 404 (390 px): no heading-order skips, unnamed links or buttons, unlabeled inputs,
  duplicate ids or missing alt text; no console errors. Touch targets raised to 44 px on phones/touch (logo, menu button, location button,
  "Read the full brief", "Clear filters", footer links).
- Not done: real-device testing, Playwright suite (not installed here), external provider link check, real-font licensing (america.gov fonts).

## Transparent favicon — November 5, 2026 (published to main)

User asked for a transparent favicon background so the bird is the only thing showing. favicon.ico (16/32/48, RGBA, corner alpha 0) and
assets/favicon.svg are now just the gold eagle with a thin near-black edge (so it stays readable on light and dark tab bars) and fill the
tab icon more. Apple touch icon (180) and manifest icons (192/512) keep the solid near-black background because iOS/Android fill transparency
themselves. ICON_VERSION bumped to 3 (links and manifest icons use ?v=3) so browsers drop the cached icon. Checked: rendered ICO sizes on light and
dark backgrounds, SVG in the browser. Not seen in a real browser tab; browsers cache favicons hard.

Footer/About wording (published to main): per the user, removed "The colors are a tribute to the state flag." from the footer note
and the matching "Its colors are a tribute to the Maryland flag, not a sign of official status." from the About page's Independent section. The
non-affiliation statements remain ("Independent, and not affiliated with or endorsed by the State of Maryland." and the About paragraph).

## Mobile menu: gold focus box and see-through overlay — November 5, 2026 (published to main)

User sent a real iPhone (Chrome) screenshot: a heavy gold box around the first menu link, and the page's footer text ghosting behind the menu.
Causes: opening the menu focused the first link (iOS draws the focus ring), and the overlay lived inside the header, which has a transform
transition and a view-transition-name (both can become the containing block for fixed children), plus a 97 percent alpha background and an
opacity fade. Fixes: the menu is now a sibling of the header at body level (position: fixed against the viewport, z-index 45, solid #121011),
revealed with a clip-path curtain instead of an opacity fade; pointer-opened menus focus the panel itself (no ring) and keyboard-opened menus
focus the first link; menu links show focus as a 3 px gold underline on the title instead of a box. Verified in the 390 px emulation: panel
covers 390x844 at body level, focus on the panel with no outline after a tap, Tab shows the underline indicator, settled menu has no page
bleed-through. Not verified on the user's actual iPhone.

## Advanced SEO — November 5, 2026 (published to main, c6ce000)

User asked for advanced SEO so Marylanders can find the site. Done in code:
- Unique titles (<= 65 chars) and descriptions (70-165) on every page. `seo_title`/`seo_description`/`nav_label` added to content/problems.json and
  content/guides.json; home, About and the two indexes are set in scripts/build.py. Home title is now "Maryland Eagles Eyes: problems to solve, help that exists".
- scripts/layout.py `page()` takes seo_title, image, image_alt, og_type, published, modified, breadcrumbs, extra. Head now has robots (max-image-preview:large),
  og:site_name/locale/image:alt/type, article times, twitter:image:alt, optional Search Console tokens from content/site.json (empty now).
- JSON-LD on every page: Organization (logo, Maryland areaServed, Buttondown sameAs), WebSite, WebPage (AboutPage/CollectionPage), BreadcrumbList; Article with
  datePublished/dateModified on briefs and guides; ItemList on /problems and /guides.
- Per-page social cards (scripts/make-social-cards.py replaces make-social-card.py): public/assets/social/<slug>.jpg (14) plus the default card.
- sitemap.xml now has lastmod (briefs/home/index 2026-11-05, guides their `checked` date, /guides the newest).
- Internal links: footer column "Open problems" (3 briefs), "More problems to explore" on each brief, open-problem link on the matching guide.
- X-Robots-Tag: noindex on /downloads/* (Word worksheets) in vercel.json. IndexNow: content/indexnow.json, public/<key>.txt, scripts/indexnow.py (dry run by default; not sent).
- tests/seo.py rewritten: lengths, uniqueness, og:image exists, JSON-LD types, Article dates, breadcrumbs, lastmod, IndexNow key, downloads header. Passes (and fails
  on a bad description, checked). Also checked in the browser pane at desktop and 375 px: footer columns, no horizontal overflow, 44 px footer targets.
- SEO_PLAYBOOK.md: owner steps (Search Console, Bing, IndexNow, links from local organizations), content roadmap, honest limits.
- Not done / needs the owner: Search Console and Bing verification and sitemap submission (account-bound), running indexnow.py --send after deploy, real
  outreach, a named editor/contact on About. No ranking guarantee. Rich-result validator and production crawl not run yet.

## "Welcome to the neighborhood" redesign — November 5, 2026 (built locally, not committed)

User asked for a better welcome section and, mid-task, that it avoid the usual vibe-coded look. A first draft (glow-dot eyebrow, shadowed rounded
photos with thick borders and gradient caption overlays, parallax drift, a "by the numbers" strip) was thrown out as generic. Final version:
- Photos are three plates on a plain grid (one tall Baltimore Inner Harbor, Annapolis and a Queen Anne's farm road at their natural landscape ratios), 6 px radius,
  no shadow, no overlay, no parallax. Captions are printed beneath: county in ink, place in grey (Baltimore City, Anne Arundel County, Queen Anne's County).
  Same grid on phones, with the tall photo going full width and the other two side by side.
- The four numbers (3 problems, 6 possible solutions, 8 guides, 24 places) became a ledger of links to /problems, /guides and the map (#help), numerals in Newsreader.
  Tap rows are 65 px+ high; gold underline on hover/focus, 2 px focus outline.
- The eyebrow reads "Welcome to <county>" once a visitor has chosen a county (site.js, uses the existing mde-county memory); it never claims local availability.
- Removed the .stats styles and drift animations; photos use the existing scroll reveal. Removed the thick gold marker underline on "twenty-four" (too stock).
Checked in the browser pane at desktop and 375 px: no horizontal overflow, ledger link targets exist, heading order unchanged, county label works. tests/seo.py passes.
Not checked: real-device Safari, reduced-motion in a real browser (CSS disables the reveal), Playwright (not installed).
