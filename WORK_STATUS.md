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
Screenshots reviewed on mobile and social preview. Production push: pending.
