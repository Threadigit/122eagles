# Design direction: "Golden hour in your neighborhood"

Written November 5, 2026, after research and before the third redesign. The first two
versions had the right structure (two doors: open problems with possible solutions, and
resource guides for problems that already have an answer) but read as a generic dark
product site: heavy sans headlines, gold accents, boxes inside boxes, one photograph.

## What the research said

- **Restraint reads as premium.** Stripe Press and Aesop (both reviewed in the browser)
  use tiny, quiet chrome, a single focal object or image, hairlines, generous space and a
  warm serif for display. Neither fills the page with bordered cards.
- **Navigation.** A centered floating "island" bar works for up to about four destinations
  (we have three plus one action). The pattern most sources recommend is hybrid: compact
  state after a little scroll, hide while scrolling down, return on scroll up. Full-screen
  menus suit mobile if closing is obvious; keyboard support is the most repeated warning
  ([patterns roundup](https://theuxshop-project.pages.dev/patterns/navigation),
  [floating nav notes](https://21st.dev/blog/react-floating-navbar-components)).
- **Movement without JavaScript.** Cross-document view transitions (`@view-transition`)
  work in Chrome 126+ and Safari 18.2+, not Firefox
  ([Chrome docs](https://developer.chrome.com/docs/web-platform/view-transitions/cross-document)).
  Scroll-driven animation (`animation-timeline`) works in Chromium 115+ and Safari 26, not
  stable Firefox ([Chrome docs](https://developer.chrome.com/docs/css-ui/scroll-driven-animations)).
  Both are progressive enhancements: guard with `@supports`, content must be correct without.
- **Clocks.** Do not put `aria-live` on a ticking time; expose the time as plain text and
  hide the seconds from assistive tech
  ([W3C WAI thread](https://lists.w3.org/Archives/Public/w3c-wai-ig/2020JulSep/0064.html)).
- **Sun maths.** NOAA's solar equations
  ([NOAA PDF](https://gml.noaa.gov/grad/solcalc/solareqns.PDF)) reproduce a published table:
  Baltimore on Nov 5, 2026 gives sunrise 6:37 AM and sunset 5:02 PM, matching
  [surf-life.blue](https://www.surf-life.blue/us/sunrisesunset/baltimore-md/202611/).
- **Type.** (Superseded: Instrument Serif turned out to be an overused AI default; see Decisions.)

## Decisions

1. **Maryland's colors, used the way maryland.gov uses them.** The state brand sheet's palette (reported by search from
   digital.maryland.gov and the Health Department's logo standards; the PDFs could not be opened here, so confirm
   against them) is red #c8122c, gold #ffc838, near-black #231f20 and white. Reviewing maryland.gov itself (November 5,
   2026) showed the state's interface is white and near-black (#1b1b1b) with grey rules and standard blue links;
   red and gold appear only inside the small flag logo mark. So here the UI is neutral (near-black and white buttons,
   grey labels) and **gold is the only brand colour used as a highlight** (hero accents, the sun, the selected
   county, link underlines). **Red is not used anywhere**, at the owner's direction. History: muted amber looked
   washed out, coral read as an alarm, sea-glass teal was unrelated to the state, and red looked off on dark and
   photographic surfaces. Because the colors look official, the footer and About page say the publication is
   independent and not affiliated with the State.
2. **Type: Newsreader and Hanken Grotesk, after america.gov.** History: Instrument Serif + Instrument Sans first (widely cited
   as an AI/vibe-coded default), then Schibsted Grotesk + Hanken Grotesk (nestpay.co's pairing), then, at the owner's request,
   the structure of america.gov: a serif for page titles and statements, a neutral grotesk for headings and text. america.gov's own
   fonts (Rhymes by Maxitype, Helvetica Now by Monotype) are commercial and licensed to that site, so they are NOT copied here.
   Free lookalikes are used instead: Newsreader (variable with optical size, SIL OFL) for page titles, big statements, numerals and
   the wordmark, and Hanken Grotesk (variable, SIL OFL) at weight 500 for smaller headings and 400 for text. All self-hosted; no
   italics anywhere. To use the real fonts, buy web licences and replace /assets/newsreader.woff2 and hanken-grotesk.woff2.
3. **The page knows what time it is.** A welcome greets the visitor by their local time and
   (once chosen) their county. A clock shows Maryland time, the visitor's own time when it
   differs, and today's sunrise and sunset. The bridge film is tinted to Maryland's actual
   sky: dawn, day, golden hour, dusk, night.
4. **Neighborhood, literally.** A real map of Maryland's 24 jurisdictions (drawn at build time from the
   simplified Census shapes: cream land on sea-glass water, a pulsing pin on your county) is the way into the
   resource guides, with a plain list of all 24 places as the keyboard and screen-reader path. Public-domain Maryland photographs
   (Library of Congress, Carol M. Highsmith) give places a face.
5. **Premium navigation.** Floating island nav with a sliding highlight, hide on scroll
   down and show on scroll up, a full-screen mobile menu, and cross-page view transitions.
6. **Movement with purpose.** Masked line reveals, stacked problem cases that settle over
   each other on desktop, a pointer-following light on interactive surfaces, slow camera
   drift on the bridge. All off under `prefers-reduced-motion`.
7. **Honest data.** County choice never invents local availability; it reminds people to
   ask which office serves them. The time-of-day greeting never claims weather.

## Emphasis and italics (revised November 5, 2026)

Italics are now a bare minimum: only quoted questions on guide pages. Emphasis inside headlines is tonal:
the emphasized clause drops to the muted ink colour (a two-tone headline), and the hero's second line is
set in gold. The greeting, map label, numerals and markers are roman. Rationale: display italics are fine
sparingly ([Cambridge brand guide](https://brand.cambridge.org/guide/typography),
[Practical Typography](https://practicaltypography.com/bold-or-italic.html)), and the owner asked for fewer.
