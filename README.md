## Current direction: problems residents can help solve

The primary entry point is `/problems`. Evidence-backed briefs distinguish published findings from proposed local projects, with a first conversation, existing services and a downloadable worksheet. `/guides` remains secondary support for people seeking help today. Subscription is secondary.

Design: "golden hour in your neighborhood" (see `DESIGN_DIRECTION.md` for the research behind it), in Maryland's brand colors used with maryland.gov-style restraint: near-black #231f20 and white for the interface (buttons are near-black on light surfaces, white on dark), grey labels, and gold #ffc838 as the one signature highlight on dark surfaces and in link underlines. Red is deliberately not used. Instrument Serif carries display type and Instrument Sans carries body and interface. Italics are used only for quoted questions; emphasis in headlines is tonal. The platform is two-fold: the **problem collection** (open gaps, each with evidence and possible solutions) and the **resource guides** (problems that already have an answer, found by county or by life area).

The homepage greets visitors by their own local time, shows Maryland's clock with today's sunrise and sunset (NOAA solar equations, computed in the browser), and tints the Bay Bridge film to Maryland's actual sky (dawn, day, golden hour, dusk, night). A county is chosen from a dropdown, the Maryland map (or the list under it) or "Use my location" (detected automatically when the visitor has already allowed location for the site). Detection runs entirely in the browser against simplified Census county shapes (`public/assets/md-counties.json`, from `scripts/prepare-counties.py`); coordinates are never sent or stored. Only the county name is remembered on the device (`localStorage`) and personalizes the greeting and `/guides`. `vercel.json` sets a Permissions-Policy that allows geolocation for this site only. On localhost, `?demo=2026-11-05T17:30` previews any Maryland wall-clock time.

## Building and previewing

```
python3 scripts/build.py     # regenerates every page, Word worksheet (needs python-docx) and the sitemap from content/*.json
python3 scripts/serve.py     # http://127.0.0.1:8012 with clean URLs and the production CSP
python3 scripts/grade-photo.py        # only when the bridge photograph or its grade changes
python3 scripts/prepare-photos.py     # only when the Maryland place photographs change
python3 scripts/prepare-counties.py  # only when the county boundary source changes
python3 scripts/make-social-card.py   # only when the social preview changes
```

Edit `content/problems.json` or `content/guides.json`, then run `build.py`. Shared page furniture (head, masthead, footer, signup dialog, eagle mark) lives in `scripts/layout.py`; page templates are in `scripts/build.py`. `public/style.css` is hand-written and is the only stylesheet. Problem proposals are untested, not active projects or promised partnerships.

County choices on `/guides` never filter results: services are delivered through local offices, so the county only adds a reminder to ask for your office. Do not add county-specific availability without a verified source.

The homepage film is CSS-only motion (transform and opacity). `public/cinema.js` only starts it after the photograph decodes and pauses it off screen; without it the photograph is simply still. `prefers-reduced-motion` turns all of it off. The ungraded photograph master is `content/source/`.

# Maryland Eagles Eyes

The publication and practical guide for **mdeagles.com**, a publication exploring challenges facing
Marylanders and practical ways to help solve them. See `EDITORIAL_DIRECTION.md`
for the Maryland Brief format, coverage areas and publishing workflow.

Static HTML and CSS with a public-domain photograph of the Chesapeake Bay Bridge. No framework or
first-party tracking scripts. Signup loads Buttondown only after a reader opens
the on-site dialog. Visual direction
inspired by The Bridge's muted landscape, serif typography and open composition;
its code and branding are not reused. The photograph is by Carol M. Highsmith,
Library of Congress; see `public/assets/PHOTO-CREDIT.md`.

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
