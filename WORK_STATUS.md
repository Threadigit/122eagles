# Maryland Eagles Eyes — continuation

The user authorized creating a GitHub repository, pushing this site, deploying
to Vercel and configuring 122eagles.com. Complete the remaining steps when secure
browser sign-ins are available. Do not change unrelated projects or DNS records.

## Completed

- Static welcome page: “Welcome to Maryland Eagles Eyes”. Original Chesapeake
  illustration, Lora/Instrument Sans typography and a muted blue-grey palette
  informed by https://www.join-thebridge.com/. Self-hosted licensed fonts.
- Local main commit `e494e5e` contains the deployed site. No JS or runtime packages.
- Local Chromium checks passed at 320, 390, 844 (short landscape), 1440 and 2560px:
  exact welcome text, fonts loaded, no horizontal overflow, reduced motion and
  no external resource requests. Reviewed phone/desktop screenshots.
- Vercel project `122eagles`, id `prj_Wmor3GXuz4VGB2Dd77qDhEQdRwY9`.
- Team `toluadetuyis-projects`, id `team_1HRMSafo3kjx8ErMiKg6Rlww`.
- Production deployment `dpl_Fn7ve4eyzhzqWVJMx22HrskhPNg9` is READY.
- Public URL: https://122eagles.vercel.app/. Served HTML exactly matches local;
  live Chromium checks passed at 390 and 1440px, including CSP, fonts and art.
- Custom domains added in Vercel and ownership verified. `www.122eagles.com`
  redirects to `122eagles.com` with status 308. DNS is NOT configured yet.
- Standard Vercel protection (`prod_deployment_urls_and_all_previews`) keeps
  preview/deployment URLs protected and the production alias public.

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

Asked the user whether to open a secure GitHub sign-in page; waiting for a reply.
Namecheap also needs a fresh sign-in. Use TinyFish start_profile_setup_session
only after consent, give the setup link and wait until the user signs in and
saves the profile. Never request passwords or verification codes in chat.

Local preview: `python3 -m http.server 8012`. Font/art/social files are committed.
No purchase, registrar transfer or nameserver migration is required.
