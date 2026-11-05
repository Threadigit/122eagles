## Current direction: problems residents can help solve

The primary entry point is `/problems`. Evidence-backed briefs distinguish published findings from proposed local projects, with a first conversation, existing services and a downloadable worksheet. `/guides` remains secondary support for people seeking help today. Subscription is secondary.

Design follows plain service-directory conventions: readable sans serif type, underlined links, simple lists and no decorative cards or animated hero. The user explicitly superseded the earlier design-preservation instruction.

Edit `content/problems.json`, then run `python3 scripts/build-problems.py` and `python3 scripts/build-guides.py`. Problem proposals are untested, not active projects or promised partnerships.

# Maryland Eagles Eyes

The publication and practical guide for **mdeagles.com**, a publication exploring challenges facing
Marylanders and practical ways to help solve them. See `EDITORIAL_DIRECTION.md`
for the Maryland Brief format, coverage areas and publishing workflow.

Static HTML and CSS with a public-domain photograph of the Chesapeake Bay Bridge. A tiny first-party
script starts the camera after the photograph decodes. No framework or
first-party tracking scripts. Signup loads Buttondown only after a reader opens
the on-site dialog. Visual direction
inspired by The Bridge's muted landscape, serif typography and open composition;
its code and branding are not reused. The photograph is by Carol M. Highsmith,
Library of Congress; see `public/assets/PHOTO-CREDIT.md`.

Preview with `python3 -m http.server 8012 --directory public`.

Vercel framework preset: Other. Production branch: `main`. Root directory:
repository root. Output directory: `public` (also set in `vercel.json`). No build
or install command is required. Website files live in `public/`; internal
continuation notes stay outside the published directory.

Push to `main` to deploy production automatically through the connected Vercel
project `122eagles` in `toluadetuyis-projects`.

Fonts: Lora and Instrument Sans, distributed under the SIL Open Font License;
see `public/assets/OFL-*.txt`. Font files are self-hosted.


Publication-update signup is connected to `https://buttondown.com/eagles` through its
supported embedded form. Readers stay on mdeagles.com; Buttondown handles
validation, confirmation and any verification inside the frame. No API key is
stored in the browser, and the public subscription endpoint is not called with
JavaScript fetch. The close button remains available throughout the flow.

Run `python3 tests/subscription-browser.py` against a local preview. Set
`EAGLES_TEST_URL` to test a deployment. Set `EAGLES_LIVE_FORM=1` to additionally
load the real Buttondown form and check email validation; this test does not
submit a subscription or send confirmation email. The other cases use a small
provider-frame fixture to exercise the website's modal behavior independently.

Set `EAGLES_LIVE_CONFIRMATION=1` for a read-only check of Buttondown's actual
confirmation preview, including message/action separation and navy buttons.
The provider owns colours inside its cross-origin frame: Settings → Design,
Custom CSS `:root { --color-action: #172b36; }`. No paid plan was enabled.
The responsive frame has enough height for confirmation; the parent dialog
scrolls on short screens with a sticky close toolbar. No outcome is auto-dismissed.

SEO: `/about` explains the Maryland focus in indexable HTML. Both pages have
canonical URLs, descriptions, social metadata and JSON-LD; `/sitemap.xml` lists
both. Run `python3 tests/seo.py` to check these links and metadata. Vercel clean
URLs serve `about.html` as `/about`; a basic Python preview uses `/about.html`.
Search Console verification and sitemap submission require the owner's Google
account. Metadata alone does not guarantee indexing or search rankings.


## Resource guide publishing

The homepage prioritizes search and browsing. `/guides` searches eight initial
resource guides by keywords and topic; URL query parameters preserve a search.
All guides are static, crawlable pages and can be browsed without JavaScript.
No external search service, account, database or tracking is required.

Edit `content/guides.json` after checking the provider source, then run
`python3 scripts/build-guides.py` to rebuild the directory, guide pages and sitemap.
The generator uses About's shared head/identity. Review the homepage's curated
links separately when adding categories or changing titles/counts. The checked
date records an actual source review; don't advance it merely because of a build.
Run `python3 tests/seo.py` and `python3 tests/discovery-browser.py`. Set
`EAGLES_TEST_URL` for the preview or live site and `EAGLES_BROWSER` for a local
Chrome executable. The preview must support clean URLs and production CSP.
CSP permits same-origin GET search forms; Buttondown remains an isolated frame.
