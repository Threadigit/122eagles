# Maryland Eagles Eyes — continuation

The user authorized creating a GitHub repository, pushing this site, deploying
to Vercel and configuring 122eagles.com. Complete the remaining steps when secure
browser sign-ins are available. Do not change unrelated projects or DNS records.

## Completed

- Static welcome page: “Welcome to Maryland Eagles Eyes”. Lora/Instrument Sans
  typography informed by https://www.join-thebridge.com/, with self-hosted fonts.
- Latest refinement replaces the generic illustration with Carol M. Highsmith’s
  public-domain aerial photograph of Maryland’s Chesapeake Bay Bridge. Warm white
  type, deep blue palette and simplified spacing; mobile receives a 960px WebP
  instead of the 1920px desktop image. Source/rights in assets/PHOTO-CREDIT.md.
  New social preview matches the photographic design.
- Latest local review passed 320/390/844 landscape/1440/2560px: exact welcome
  text, image delivery, fonts, no horizontal overflow and no external runtime
  requests. Throttled Chromium mobile: FCP 0.62s, CLS 0.00082, transfer ~220KB
  excluding social-preview image. These are local lab results, not field data.
- Site commit `c1f0bd8` contains the current deployed design. No JS or runtime packages.
- Local Chromium checks passed at 320, 390, 844 (short landscape), 1440 and 2560px:
  exact welcome text, fonts loaded, no horizontal overflow, reduced motion and
  no external resource requests. Reviewed phone/desktop screenshots.
- Vercel project `122eagles`, id `prj_Wmor3GXuz4VGB2Dd77qDhEQdRwY9`.
- Team `toluadetuyis-projects`, id `team_1HRMSafo3kjx8ErMiKg6Rlww`.
- Current production deployment `dpl_8GGNcGEiWKMSTdPnKHLLdPA9net3` is READY.
  Live phone/desktop checks passed for the final polish at commit `c1f0bd8`.
- Public URL: https://122eagles.vercel.app/. Served HTML exactly matches local;
  live Chromium checks passed at 390 and 1440px, including CSP, fonts and art.
- Custom domains added in Vercel and ownership verified. `www.122eagles.com`
  redirects to `122eagles.com` with status 308. DNS is NOT configured yet.
- Standard Vercel protection (`prod_deployment_urls_and_all_previews`) keeps
  preview/deployment URLs protected and the production alias public.

- Final polish: refined letter spacing and consistent phone/tablet type scale,
  softer image shading, an 850ms entrance (disabled for reduced motion), and an
  increased-contrast treatment. Seven viewport checks (320–2560px), entrance
  completion and contrast preference checks pass.

## Remaining

1. Create a private GitHub repo `adetuyiTolu/122eagles`, empty; then push main.
   Both `gh repo create` (GraphQL) and REST POST /user/repos returned 403
   Resource not accessible by integration. The app can read user identity and
   push existing repositories; it cannot create repositories.
2. Link the existing Vercel project to this GitHub repo for automatic deployments.
   `create_git_project` does not reconnect existing unlinked projects; use Vercel
   project Git settings/browser or a supported API, once the repo exists.
3. In Namecheap Advanced DNS, inspect and save the existing DNS baseline first.
   Replace only apex parking/redirect records and www parking CNAME as needed.
   Preserve MX, SPF, DKIM, verification TXT and unrelated host records.
4. Latest project-specific Vercel DNS recommendation, obtained after adding the
   domains: apex A values `216.198.79.1` and `64.29.17.1` (rank 1), www CNAME
   `6320fd3e556bc659.vercel-dns-017.com.` (rank 1). Recheck these with
   get_domain_config before saving. Authoritative nameservers remain
   dns1.registrar-servers.com / dns2.registrar-servers.com (Namecheap).
   Public apex currently returns 192.64.119.118; www is parkingpage.namecheap.com.
5. Verify DNS, Vercel domain configuration, HTTPS and www redirect, and test the
   page on https://122eagles.com/ after propagation. Do not claim it is live there
   until verified.

## Browser sign-in blocker

TinyFish Default profile id: `prof_f047cdc863044f54`. User confirmed both GitHub
and Namecheap were signed in, but both browser runs redirected to login. No
records changed and no repository created. GitHub run
`26bbf298-c654-4853-a11e-17e56cec5129` and Namecheap inspection
`d2a65b0e-80db-40e5-bff3-850394ecb84c` are completed, not pending.

User requested the final visual refinement and domain configuration. A secure
Namecheap profile setup was opened in TinyFish; waiting for the user to sign in,
click Save profile, and reply saved. Do not run Namecheap automation until saved.
GitHub still needs a fresh sign-in or user-created empty repository. Use TinyFish start_profile_setup_session
only after consent, give the setup link and wait until the user signs in and
saves the profile. Never request passwords or verification codes in chat.

Local preview: `python3 -m http.server 8012`. Font/art/social files are committed.
No purchase, registrar transfer or nameserver migration is required.

## Latest Namecheap attempt

The user replied Saved after the secure Default-profile setup. Automation run
`6a06d4eb-dfbd-4af3-a9bb-59cfd2e4012b` nevertheless opened signed out; the run
completed without changing DNS. Default profile domain count increased to 10 but
signed_in_sites remains empty. A dedicated Namecheap profile is being created
with the Advanced DNS URL so the authenticated app page can load before saving.
Public DNS baseline is /tmp/122eagles-dns-before.json; five email-forwarding MX
records and the forwarding SPF TXT must remain unchanged.

Dedicated retry profile: `prof_91ba5a2dbbf740e2`, name Namecheap — 122eagles.
Setup page was sent to the user, who must reach the actual Advanced DNS page
then click Save profile and reply Saved. A text-input request is pending for
that confirmation. Run DNS automation on this exact dedicated profile after
confirmation; do not keep retrying Default. No secure setup URLs are committed.

## Dedicated-profile result

The user replied Saved for the dedicated profile. Run
`af237b5a-a542-4f08-be39-ac7b96f884eb` completed on the Namecheap login page.
No DNS records changed. list_profiles showed domain_count 0 for this dedicated
profile before the run. Neither Default nor dedicated profile has supplied an
active Namecheap session to automation after user-confirmed saves. Do not send
the user through another identical setup/save loop without a concrete new fix.

Direct fallback supplied: Namecheap > 122eagles.com > Advanced DNS > Host Records:
A @ 216.198.79.1; A @ 64.29.17.1; CNAME www
6320fd3e556bc659.vercel-dns-017.com; Automatic TTL. Replace only conflicting
apex parking/URL redirect and www parking records. Preserve mail/other records.
After the user applies these, verify public DNS, Vercel configuration, HTTPS and
www-to-apex redirect. Domain and GitHub repository setup remain unfinished.
