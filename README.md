## Current direction: problems residents can help solve

The primary entry point is `/problems`. Evidence-backed briefs distinguish published findings from proposed local projects, with a first conversation, existing services and a downloadable worksheet. `/guides` remains secondary support for people seeking help today. Subscription is secondary.

Design: "golden hour in your neighborhood" (see `DESIGN_DIRECTION.md` for the research behind it), in Maryland's brand colors used with maryland.gov-style restraint: near-black #231f20 and white for the interface (buttons are near-black on light surfaces, white on dark), grey labels, and gold #ffc838 as the one signature highlight on dark surfaces and in link underlines. Red is deliberately not used. Newsreader (a serif, for page titles and big statements) and Hanken Grotesk (for smaller headings, text and interface) follow the structure of america.gov using free, self-hosted, variable SIL OFL fonts; america.gov's own Rhymes and Helvetica Now are commercial and are not copied. Italics are used only for quoted questions; emphasis in headlines is tonal. The platform is two-fold: the **problem collection** (open gaps, each with evidence and possible solutions) and the **resource guides** (problems that already have an answer, found by county or by life area).

The homepage greets visitors by their own local time, shows Maryland's clock with today's sunrise and sunset (NOAA solar equations, computed in the browser), and tints the Bay Bridge film to Maryland's actual sky (dawn, day, golden hour, dusk, night). A county is chosen from a dropdown, the Maryland map (or the list under it) or "Use my location" (detected automatically when the visitor has already allowed location for the site). Detection runs entirely in the browser against simplified Census county shapes (`public/assets/md-counties.json`, from `scripts/prepare-counties.py`); coordinates are never sent or stored. Only the county name is remembered on the device (`localStorage`, with a source: `auto` for a county found from location, `manual` for one the visitor chose) and personalizes the greeting and `/guides`. On load, if location is already allowed, an `auto` county is re-checked so it follows the visitor; a `manual` county or `?county=` in the address is never overridden, and nothing is asked on load. `vercel.json` sets a Permissions-Policy that allows geolocation for this site only. On localhost, `?demo=2026-11-05T17:30` previews any Maryland wall-clock time.

## Building and previewing

```
python3 scripts/build.py     # regenerates every page, Word worksheet (needs python-docx) and the sitemap from content/*.json
python3 scripts/serve.py     # http://127.0.0.1:8012 with clean URLs and the production CSP
python3 scripts/grade-photo.py        # only when the bridge photograph or its grade changes
python3 scripts/prepare-photos.py     # only when the Maryland place photographs change
python3 scripts/prepare-counties.py  # only when the county boundary source changes
python3 scripts/make-favicons.py     # only when the logo or favicon colours change (then bump ICON_VERSION in scripts/layout.py and the ?v= in site.webmanifest, or browsers keep showing the old icon)
python3 scripts/make-social-cards.py  # only when a page title or the social look changes (one 1200x630 card per page in public/assets/social/)
python3 tests/seo.py                  # titles, descriptions, social cards, JSON-LD, sitemap lastmod (run after build.py)
python3 scripts/indexnow.py           # dry run; add --send AFTER a deploy to ping Bing and other IndexNow engines
```

Edit `content/problems.json` or `content/guides.json`, then run `build.py`. Shared page furniture (head, masthead, footer, signup dialog, eagle mark) lives in `scripts/layout.py`; page templates are in `scripts/build.py`. `public/style.css` is hand-written and is the only stylesheet. Problem proposals are untested, not active projects or promised partnerships.

County choices on `/guides` never filter results: services are delivered through local offices, so the county only adds a reminder to ask for your office. Do not add county-specific availability without a verified source.

The homepage film is CSS-only motion (transform and opacity). `public/cinema.js` only starts it after the photograph decodes and pauses it off screen; without it the photograph is simply still. `prefers-reduced-motion` turns all of it off. The ungraded photograph master is `content/source/`.

# Maryland Eagles Eyes

The publication and practical guide for **mdeagles.com**, a publication exploring challenges facing
Marylanders and practical ways to help solve them. See `EDITORIAL_DIRECTION.md`
for the Maryland Brief format, coverage areas and publishing workflow.

Static HTML and CSS with a public-domain photograph of the Chesapeake Bay Bridge. No framework or
first-party tracking scripts. Signup loads nothing from Buttondown until a reader submits
the on-site form. Visual direction
inspired by The Bridge's muted landscape, serif typography and open composition;
its code and branding are not reused. The photograph is by Carol M. Highsmith,
Library of Congress; see `public/assets/PHOTO-CREDIT.md`.

Vercel framework preset: Other. Production branch: `main`. Root directory:
repository root. Output directory: `public` (also set in `vercel.json`). No build
or install command is required. Website files live in `public/`; internal
continuation notes stay outside the published directory.

Push to `main` to deploy production automatically through the connected Vercel
project `122eagles` in `toluadetuyis-projects`.

Fonts: Newsreader and Hanken Grotesk, distributed under the SIL Open Font License;
see `public/assets/OFL-*.txt`. Font files are self-hosted.


Publication-update signup is our own form in an on-site dialog (`scripts/layout.py`, `public/subscribe.js`). It posts the
email address straight to Buttondown's embed endpoint (`https://buttondown.com/api/emails/embed-subscribe/eagles`, fields `email`
and `embed=1`) and Buttondown opens its own confirmation in a small window (a new tab if the browser blocks popups; without
JavaScript the form still posts in a new tab). Nothing from Buttondown loads until a reader submits, and no API key is involved.
The form is ours because Buttondown's framed page cannot be styled without its Custom CSS (not on this plan) and cannot be fonted
or recoloured from outside. `vercel.json` allows `form-action https://buttondown.com` and no longer allows any frames.

`python3 tests/subscription-browser.py` (Playwright; run against a local preview, set `EAGLES_TEST_URL` for a deployment)
answers every Buttondown request with a local fixture, so it never subscribes anyone or sends email. Not yet run: Playwright
is not installed here. A real end-to-end signup (the address added and the confirmation email arriving) needs a manual check
with an address you own.

SEO: every page has a unique title (65 characters or fewer) and description, a canonical URL, a robots meta
that allows large image previews, Open Graph and Twitter tags with its own social card, and JSON-LD
(Organization, WebSite, WebPage, BreadcrumbList, plus Article on briefs and guides and ItemList on the two
indexes). `seo_title` and `seo_description` live beside each entry in `content/problems.json` and
`content/guides.json`; the other titles are set in `scripts/build.py`. `/sitemap.xml` carries `lastmod` from the
content dates (briefs 2026-11-05, guides their `checked` date). `/downloads/*` carries `X-Robots-Tag: noindex` so the
Word worksheets do not compete with the briefs. `python3 tests/seo.py` enforces all of this. Owner steps that need
a Google or Bing account (Search Console, Webmaster Tools) are in `SEO_PLAYBOOK.md`. Metadata alone does not
guarantee indexing or rankings.


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
CSP permits same-origin GET search forms; Buttondown receives the signup form post (`form-action`).
