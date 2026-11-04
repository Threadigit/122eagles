# Maryland Eagles Eyes — continuation

The user authorized building this welcome page, creating/pushing a GitHub repo,
deploying to Vercel and configuring 122eagles.com. Preserve the simple welcome
scope, current bridge photograph and design. Read before continuing.

## Site and domain — complete

- Site: https://122eagles.com/ ; Vercel alias https://122eagles.vercel.app/.
- Exact heading: Welcome to Maryland Eagles Eyes.
- Public-domain photograph of Maryland's Chesapeake Bay Bridge, Carol M.
  Highsmith / Library of Congress. See assets/PHOTO-CREDIT.md. Responsive WebP
  assets and self-hosted Lora/Instrument Sans fonts; no JS, tracking or packages.
- User requested motion: staggered welcome/Maryland/Eagles Eyes entrance plus
  gentle mirrored wing movement and slight lift on the eagle every 10 seconds.
  Most of the cycle rests. All animation uses opacity/transform and is disabled
  for reduced motion. User subsequently requested cinematic bridge motion: the
  photograph now has a slow 28-second alternating camera pan/zoom. The bridge
  structure does not deform, text stays steady, and no image edge is exposed.
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

## Hosting

- Vercel project 122eagles / prj_Wmor3GXuz4VGB2Dd77qDhEQdRwY9.
- Team toluadetuyis-projects / team_1HRMSafo3kjx8ErMiKg6Rlww.
- Static HTML/CSS, framework Other/null, no install/build commands, repo root.
- Text/eagle animation deployment dpl_JB3mRJ5igcWqcbumNYysnrhVo4ZR was READY.
  Actual apex checks passed normal and reduced motion; www HTTPS redirect passed.
  Current cinematic deployment dpl_AMM8EUYzNw5VoVs6Lg4tg4Un6yyW is READY
  (site commit d90188f). Live mobile/desktop checks verify actual camera movement
  and reduced-motion behaviour. Local checks at 320/390/1440/2560 verify all
  pan/zoom positions cover the frame and the heading geometry remains fixed.
- Standard Vercel protection prod_deployment_urls_and_all_previews; production
  aliases/custom domains public, previews/deployment URLs protected.

## GitHub — still blocked

- Intended private repo: adetuyiTolu/122eagles. Local main has all source commits.
- GitHub app/gh cannot create repositories: GraphQL and REST returned403 Resource
  not accessible by integration. The app can push existing authorized repos.
- Latest browser creation attempt 7e995fd7-27d6-4bd0-b2d8-dc71b8194d27 completed
  at GitHub login. No repo created. Needs a saved GitHub sign-in or user-created
  empty repository before push/linking. Do not ask for passwords in chat.
- Once repo exists, push main then connect the EXISTING Vercel project in its Git
  settings. create_git_project does not reconnect an existing unlinked project.

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

Local preview: python3 -m http.server 8012. No registrar transfer, nameserver
migration or purchase is needed. Do not change other projects or records.
