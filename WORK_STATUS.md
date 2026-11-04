# Maryland Eagles Eyes — continuation

The user authorized building this welcome page, creating/pushing a GitHub repo,
deploying to Vercel and configuring 122eagles.com. Preserve the simple welcome
scope, current bridge photograph and design. Read before continuing.

## Site and domain — complete

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

## Newsletter copy and subscription CTA — in progress

User requested the exact new copy:
“Maryland, made clear.” / “Our eyes stay on the policies, projects and programs
shaping the state, so you see what’s coming and what it means for your money,
your home and your business.” / “Five minutes. Free. Every week.” / CTA “Open
your eyes”, which must subscribe readers.

Local feature branch feat/maryland-newsletter-signup adds this beneath the
animated publication name, tighter responsive heading/spacing to fit, updated
meta descriptions and a single warm-white CTA. Reviewed 320/390/844 landscape/
1440px with no horizontal overflow; the CTA is visible above the fold on phones.
Button is deliberately disabled ONLY in the unpublished draft until a real
signup destination is connected. Do not merge or publish a disabled/fake signup.
No newsletter environment variables or integrations exist in this Vercel project.

User asked for help setting up a newsletter service. Official beehiiv pricing
currently says free forever up to2500 subscribers, unlimited sends and free
external signup forms (https://www.beehiiv.com/pricing and
https://www.beehiiv.com/features/subscribe-forms). Recommended that free plan.
A preference question is pending: new free beehiiv account or existing account.
After they choose, open a secure provider signup/sign-in setup session, wait for
user save, then configure Maryland Eagles Eyes and obtain its actual signup
form/link. No paid plan, paid trial or billing details should be selected.
Use the real form to wire CTA and verify success/confirmation behavior without
sending unsolicited test emails. Signup must work before merging to main.
