# SEO playbook for mdeagles.com

Written November 5, 2026. Goal: Marylanders searching for help, or for problems to work on, find this site. Nothing here
guarantees rankings. Search engines decide that, and a new site with three briefs and eight guides starts small. What the code
can do is make every page easy to crawl, understand and share. That is done. What is left is mostly steps only the owner
can take, and a content habit.

## What the site already does (in the code)

- One unique `<title>` and meta description per page, written around what a Marylander would type ("Maryland energy bill
  help", "Find child care in Maryland"). Titles are 65 characters or fewer, descriptions 70–165. `tests/seo.py` enforces it.
- Canonical URLs, `robots` meta with large image previews, `og:` and Twitter tags, and **a social card per page**
  (`public/assets/social/`), so a link shared in a text, WhatsApp or Facebook group shows the page's own title.
- Structured data on every page: Organization (name, logo, Maryland service area), WebSite, WebPage, BreadcrumbList. Briefs
  and guides also carry Article with published and modified dates. The two index pages carry an ItemList.
- `sitemap.xml` with `lastmod`, `robots.txt` pointing to it, `X-Robots-Tag: noindex` on the Word worksheets, 404 page excluded.
- Internal links: every page links to all briefs and all guides through the footer; briefs list the other briefs; guides link
  to related guides and to the open problem that matches.
- Fast, crawlable HTML with no client-side rendering needed for content, self-hosted fonts, responsive images.

## Steps only you can do

1. **Google Search Console** (free): add `https://mdeagles.com` as a Domain property, verify through DNS (a TXT record at your
   DNS provider; you already manage DNS for the domain), then *Sitemaps → submit* `sitemap.xml`. Use *URL inspection → Request
   indexing* on the home page and each brief and guide once. If you prefer the "URL prefix" method, put the token in
   `content/site.json` (`google_site_verification`), run `python3 scripts/build.py`, deploy, then verify.
2. **Bing Webmaster Tools** (free): sign in, import the site from Search Console (easiest), or paste the token into
   `content/site.json` (`bing_site_verification`). Bing powers DuckDuckGo, Yahoo and ChatGPT search results too.
3. **IndexNow** (Bing, Yandex and others): after a deploy, run `python3 scripts/indexnow.py --send`. Google does not use it.
4. **Check both consoles weekly for the first month.** The *Pages* report tells you what is indexed and why anything is not;
   the *Performance* report shows the queries people actually use. Those queries are the best content roadmap you will have.
5. **Check redirects.** `122eagles.com` and `www.122eagles.com` already redirect to `mdeagles.com`. In Search Console, also
   add `www.mdeagles.com` and confirm it redirects to the main site (not yet checked here).

## Getting found by Marylanders (the part that moves rankings)

Search engines rank sites that other credible sites link to. For a local public-interest site that means people, not tricks.

- **Ask for links from places that already serve these readers**: county library systems and branch pages, community
  and neighborhood associations, the Baltimore and county nonprofit directories, college basic-needs and career centers,
  chambers of commerce and small-business groups (they are the audience for the small-business brief), immigrant-serving
  organizations (for the careers brief), local newsletters and reporters who cover these topics. Offer a specific page
  ("our guide to applying for energy assistance") and do not ask for a generic homepage link.
- **Be a source, not a spammer.** Do not buy links, do not submit to link farms, do not post the same link everywhere.
- **Claim profiles that carry a link**: a Buttondown archive page for the newsletter (already linked from the site's
  structured data), social profiles, and a Google Business Profile *only if* you have a real, staffed local presence.
  Do not create a fake address.
- **E-E-A-T (trust)**: the About page says who we are and that we are independent. Add a named editor and a contact
  address or form when you are comfortable publishing them. Search engines and readers trust pages with a visible
  human behind them. I have not published any personal email address.
- **Share the social cards**: every brief and guide now has its own preview image, which lifts click-through from texts,
  Facebook groups, Nextdoor, LinkedIn and Reddit (r/maryland, r/baltimore, county subreddits).

## Content roadmap (ordered by likely payoff)

1. **More guides for the questions Marylanders ask most.** Each guide is a page that can rank. Strong candidates, each of which
   should be sourced from the provider and dated like the existing ones: SNAP / food assistance, Medicaid renewal, WIC,
   unemployment insurance, DMV and MVA services, expungement and legal aid, free tax help (VITA), driver's license for
   immigrants, home repair and weatherization, senior services. Keep the "checked on" date current. Stale guides lose trust.
2. **Briefs with local evidence.** Each new brief should answer a question people search: what is the problem here, what does
   the data say, what could help.
3. **County hubs, carefully.** A page per county (24) would match "help in Prince George's County" searches. Do this only
   with verified county-specific information (the site deliberately does not claim local availability today). Thin pages that
   only swap the county name are treated as spam, so each hub needs real local content or nothing.
4. **Spanish-language versions** of the top guides (and then Haitian Creole, Amharic, Korean and others by demand). It
   meets large Maryland audiences who are underserved by English-only help pages. It needs a human translator or reviewer
   and `hreflang` tags (not built yet; add them with the first translated page).
5. **Refresh and re-submit.** When a guide is re-checked, update its `checked` date in `content/guides.json`, rebuild, deploy,
   and run IndexNow. The sitemap `lastmod` follows automatically.

## What to expect, honestly

- A new domain usually takes days to a few weeks to be crawled and weeks to months to settle in results. Submitting the
  sitemap speeds up discovery, not ranking.
- Searches like "Maryland energy assistance" are crowded by state agency sites. We compete on being clearer, more
  specific (county, step by step) and on pairing help with context, not on outranking maryland.gov.
- Measure with Search Console impressions, clicks and queries. There is no analytics script on the site (by design); add
  a privacy-respecting one only if you need visit counts, and it needs a CSP change.
