"""Shared page furniture for the MD Eagles generators.

Every page is built from the same head, masthead, footer and signup dialog so the
two build scripts cannot drift apart. No runtime dependencies.
"""
import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / 'public'
SITE = 'https://mdeagles.com'
SOCIAL_IMAGE = SITE + '/assets/social-mdeagles.jpg'


def e(value):
    return html.escape(value, quote=True)


# The eagle mark. Same geometry as assets/eagle.svg, split into two wings and a
# body so the homepage film can move the wings. Inherits colour from the page.
def eagle(css_class='eagle', stroke_width='2'):
    return (
        f'<svg class="{css_class}" viewBox="6 20 52 27" fill="none" stroke="currentColor" '
        f'stroke-width="{stroke_width}" stroke-linejoin="round" stroke-linecap="round" '
        'aria-hidden="true" focusable="false">'
        '<g class="eagle-wing eagle-wing-l"><path pathLength="1" d="M32 38 22 26 8 22 19 37 32 45"/></g>'
        '<g class="eagle-wing eagle-wing-r"><path pathLength="1" d="M32 38 42 26 56 22 45 37 32 45"/></g>'
        '<g class="eagle-body"><path pathLength="1" d="m27 32 5-8 5 8M32 38v7"/></g>'
        '</svg>'
    )


NAV = [
    ('problems', '/problems', 'Problem collection', 'Problems'),
    ('guides', '/guides', 'Resource guides', 'Guides'),
    ('about', '/about', 'About', 'About'),
]

COUNTIES = [
    'Allegany', 'Anne Arundel', 'Baltimore City', 'Baltimore County', 'Calvert', 'Caroline', 'Carroll',
    'Cecil', 'Charles', 'Dorchester', 'Frederick', 'Garrett', 'Harford', 'Howard', 'Kent', 'Montgomery',
    "Prince George's", "Queen Anne's", "St. Mary's", 'Somerset', 'Talbot', 'Washington', 'Wicomico', 'Worcester',
]


def county_options(placeholder='Choose your county'):
    return f'<option value="">{placeholder}</option>' + ''.join(
        f'<option value="{e(c)}">{e(c)}</option>' for c in COUNTIES)


def masthead(current=None):
    links = ''.join(
        '<a href="%s"%s><span class="nav-long">%s</span><span class="nav-short" aria-hidden="true">%s</span></a>'
        % (href, ' aria-current="page"' if key == current else '', long, short)
        for key, href, long, short in NAV
    )
    return (
        '<header class="masthead"><div class="masthead-inner">'
        f'<a class="identity" href="/">{eagle("identity-mark")}<span>MD Eagles</span></a>'
        f'<nav aria-label="Main navigation">{links}</nav>'
        '</div></header>'
    )


def footer():
    guides = json.loads((ROOT / 'content/guides.json').read_text())
    help_links = ''.join(f'<a href="/guides/{g["slug"]}">{e(g["category"])}</a>' for g in guides)
    return (
        '<footer class="site-footer night"><div class="footer-inner">'
        f'<div class="footer-brand"><a class="identity" href="/">{eagle("identity-mark")}<span>MD Eagles</span></a>'
        '<p>Maryland Eagles Eyes is an independent publication. We document the gaps in everyday Maryland life, '
        'and point residents to the help that already exists.</p></div>'
        '<nav class="footer-col" aria-label="Explore"><h2>Explore</h2><a href="/problems">Problem collection</a>'
        '<a href="/guides">Resource guides</a><a href="/about">About</a><a href="/#subscribe">Email updates</a></nav>'
        f'<nav class="footer-col" aria-label="Resource guides by need"><h2>Find help with</h2>{help_links}</nav>'
        '<p class="footer-credit">Bay Bridge photograph by Carol M. Highsmith, Library of Congress, public domain. '
        '<a href="https://hdl.loc.gov/loc.pnp/highsm.14292">Source record</a></p>'
        '</div></footer>'
    )


def band(title, lead='', crumb='', pos=1, extra=''):
    """A dark, still crop of the bridge that opens every inner page."""
    return (
        f'<section class="band night band-pos-{pos}">'
        '<img class="band-img" src="/assets/bay-bridge-film-960.webp" '
        'srcset="/assets/bay-bridge-film-960.webp 960w, /assets/bay-bridge-film-1920.webp 1920w" '
        'sizes="100vw" width="960" height="878" alt="" decoding="async">'
        '<div class="band-shade"></div><div class="band-inner">'
        f'{crumb}<h1>{title}</h1>{lead}{extra}</div></section>'
    )


def subscribe_dialog():
    return '''<dialog id="subscribe-dialog" class="subscribe-dialog" aria-labelledby="subscribe-title" aria-describedby="subscribe-description">
    <div class="subscribe-toolbar">
    <p class="subscribe-eyebrow">Maryland Eagles Eyes</p>
    <button class="subscribe-close" type="button" aria-label="Close signup" data-close-subscribe><svg width="19" height="19" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><path d="m6 6 12 12M18 6 6 18"/></svg></button>
    </div>
    <div class="subscribe-content">
    <h2 id="subscribe-title">Hear when a new problem is published.</h2>
    <p id="subscribe-description">Free email when we publish a new brief or a follow-up. Unsubscribe anytime.</p>
    <div class="signup-embed">
      <iframe data-subscribe-frame data-src="https://buttondown.com/eagles?as_embed=true" title="Email signup for Maryland Eagles Eyes" referrerpolicy="strict-origin-when-cross-origin"></iframe>
      <p class="signup-consent">Receive Maryland Eagles Eyes by email. Unsubscribe at any time.</p>
      <button class="signup-reload" type="button">Reload signup form</button>
    </div>
    </div>
  </dialog>'''


def schema_graph(title, desc, path, kind='WebPage', home=False):
    page = {'@type': kind, 'name': title, 'description': desc, 'url': SITE + path,
            'inLanguage': 'en-US', 'isPartOf': {'@id': SITE + '/#website'}}
    graph = [page]
    if home:
        graph = [
            {'@type': 'WebSite', '@id': SITE + '/#website', 'name': 'Maryland Eagles Eyes',
             'alternateName': 'MD Eagles', 'url': SITE + '/', 'inLanguage': 'en-US'},
            {'@type': 'Organization', '@id': SITE + '/#organization', 'name': 'Maryland Eagles Eyes',
             'alternateName': 'MD Eagles', 'url': SITE + '/', 'logo': SITE + '/assets/eagle.svg'},
            page,
        ]
    return json.dumps({'@context': 'https://schema.org', '@graph': graph}, ensure_ascii=False)


def page(title, desc, path, body, *, current=None, body_class='', scripts=(), kind='WebPage',
         home=False, dialog=False):
    full_title = f'{title} | MD Eagles'
    script_tags = ''.join(f'<script src="{s}" defer></script>' for s in scripts)
    head = (
        '<!DOCTYPE html><html lang="en-US"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width, initial-scale=1">'
        '<meta name="theme-color" content="#07141b">'
        f'<title>{e(full_title)}</title><meta name="description" content="{e(desc)}">'
        f'<link rel="canonical" href="{SITE}{path}">'
        f'<meta property="og:title" content="{e(full_title)}"><meta property="og:description" content="{e(desc)}">'
        f'<meta property="og:url" content="{SITE}{path}"><meta property="og:type" content="website">'
        f'<meta property="og:image" content="{SOCIAL_IMAGE}"><meta property="og:image:width" content="1200">'
        '<meta property="og:image:height" content="630">'
        '<meta name="twitter:card" content="summary_large_image">'
        f'<meta name="twitter:title" content="{e(full_title)}"><meta name="twitter:description" content="{e(desc)}">'
        f'<meta name="twitter:image" content="{SOCIAL_IMAGE}">'
        '<link rel="icon" href="/assets/eagle.svg"><link rel="stylesheet" href="/style.css">'
        f'<script type="application/ld+json">{schema_graph(title, desc, path, kind, home)}</script></head>'
    )
    classes = f' class="{body_class}"' if body_class else ''
    return (
        f'{head}<body{classes}><a class="skip-link" href="#main">Skip to content</a>'
        f'{masthead(current)}<main id="main">{body}</main>{footer()}'
        f'{subscribe_dialog() if dialog else ""}{script_tags}</body></html>'
    )
