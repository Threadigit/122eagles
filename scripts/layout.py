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
# Browsers cache favicons very hard. Bump this whenever an icon changes so they fetch the new one.
ICON_VERSION = '3'


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


def typo(text):
    """Typographic apostrophes for display (values and URLs keep the plain character)."""
    return text.replace("'", '\u2019')


def county_options(placeholder='Choose your county'):
    return f'<option value="">{placeholder}</option>' + ''.join(
        f'<option value="{e(c)}">{e(typo(c))}</option>' for c in COUNTIES)


# Public-domain photographs by Carol M. Highsmith (Library of Congress), see PHOTO-CREDIT.md.
PLACES = {
    'bridge': ('Chesapeake Bay Bridge', 'https://hdl.loc.gov/loc.pnp/highsm.14292'),
    'baltimore': ('Baltimore’s Inner Harbor', 'https://www.loc.gov/pictures/collection/highsm/item/2011634087/'),
    'annapolis': ('Harbor at Annapolis', 'https://www.loc.gov/pictures/collection/highsm/item/2011634876/'),
    'farm': ('A working farm in Queen Anne’s County', 'https://www.loc.gov/pictures/collection/highsm/item/2018697913/'),
    'sunset': ('Chesapeake Bay sunset', 'https://www.loc.gov/pictures/collection/highsm/item/2011630543/'),
}
PLACE_FILES = {
    'baltimore': 'baltimore-inner-harbor', 'annapolis': 'annapolis-harbor',
    'farm': 'eastern-shore-farm-road', 'sunset': 'chesapeake-sunset',
}


def place_img(key, css_class, sizes='100vw', eager=False):
    """An <img> for one of the place photographs (key in PLACE_FILES)."""
    from PIL import Image  # build-time only
    slug = PLACE_FILES[key]
    files = sorted((PUBLIC / 'assets' / 'places').glob(f'{slug}-*.webp'), key=lambda f: int(f.stem.rsplit('-', 1)[1]))
    widths = [int(f.stem.rsplit('-', 1)[1]) for f in files]
    with Image.open(files[-1]) as im:
        w, h = im.size
    srcset = ', '.join(f'/assets/places/{slug}-{width}.webp {width}w' for width in widths)
    loading = '' if eager else ' loading="lazy"'
    return (f'<img class="{css_class}" src="/assets/places/{slug}-{widths[0]}.webp" srcset="{srcset}" '
            f'sizes="{sizes}" width="{w}" height="{h}" alt=""{loading} decoding="async">')


def masthead(current=None):
    links = ''.join(
        '<a href="%s"%s>%s</a>' % (href, ' aria-current="page"' if key == current else '', long)
        for key, href, long, short in NAV
    )
    menu_links = ''.join(
        '<a href="%s"%s><span class="menu-title">%s</span><span class="menu-note">%s</span></a>'
        % (href, ' aria-current="page"' if key == current else '', long, note)
        for (key, href, long, short), note in zip(NAV, [
            'Open problems, with possible solutions',
            'Help that already exists, by county or need',
            'How we choose and source our briefs'])
    )
    return (
        '<header class="masthead" data-masthead><div class="island">'
        f'<a class="identity" href="/">{eagle("identity-mark")}<span>MD Eagles</span></a>'
        f'<nav class="island-nav" aria-label="Main navigation" data-island-nav><span class="island-pill" aria-hidden="true"></span>{links}</nav>'
        '<a class="island-cta" href="/#subscribe">Email updates</a>'
        '<button class="menu-toggle" type="button" aria-expanded="false" aria-controls="site-menu" data-menu-toggle>'
        '<span class="menu-toggle-label">Menu</span><span class="menu-toggle-icon" aria-hidden="true"><i></i><i></i></span></button>'
        '</div></header>'
        '<div class="menu" id="site-menu" data-menu tabindex="-1" hidden>'
        f'<nav class="menu-nav" aria-label="Mobile">{menu_links}<a href="/#subscribe"><span class="menu-title">Email updates</span>'
        '<span class="menu-note">A note when a new problem is published</span></a></nav>'
        '<p class="menu-foot"><time data-md-clock>Maryland</time><span data-menu-county></span></p>'
        '</div>'
    )


def footer():
    guides = json.loads((ROOT / 'content/guides.json').read_text())
    help_links = ''.join(f'<a href="/guides/{g["slug"]}">{e(g["category"])}</a>' for g in guides)
    problems = json.loads((ROOT / 'content/problems.json').read_text())
    problem_links = ''.join(f'<a href="/problems/{x["slug"]}">{e(x["nav_label"])}</a>' for x in problems)
    return (
        '<footer class="site-footer night"><div class="footer-inner">'
        f'<div class="footer-brand"><a class="identity" href="/">{eagle("identity-mark")}<span>MD Eagles</span></a>'
        '<p class="footer-line">Twenty-four places. One Maryland.</p>'
        '<p>Maryland Eagles Eyes is an independent publication. We document the gaps in everyday Maryland life, '
        'and point residents to the help that already exists.</p>'
        '<p class="footer-note">Independent, and not affiliated with or endorsed by the State of Maryland.</p></div>'
        '<nav class="footer-col" aria-label="Explore"><h2>Explore</h2><a href="/problems">Problem collection</a>'
        '<a href="/guides">Resource guides</a><a href="/about">About</a><a href="/#subscribe">Email updates</a></nav>'
        f'<nav class="footer-col" aria-label="Open problems"><h2>Open problems</h2>{problem_links}</nav>'
        f'<nav class="footer-col" aria-label="Resource guides by need"><h2>Find help with</h2>{help_links}</nav>'
        '</div></footer>'
    )


def band(title, lead='', crumb='', pos=1, extra='', place='bridge'):
    """A dark, still crop of a Maryland photograph that opens every inner page."""
    if place == 'bridge':
        image = ('<img class="band-img" src="/assets/bay-bridge-film-960.webp" '
                 'srcset="/assets/bay-bridge-film-960.webp 960w, /assets/bay-bridge-film-1920.webp 1920w" '
                 'sizes="100vw" width="960" height="878" alt="" decoding="async">')
    else:
        image = place_img(place, 'band-img', eager=True)
    name, url = PLACES[place]
    return (
        f'<section class="band night band-pos-{pos}">{image}'
        '<div class="band-shade"></div><div class="band-inner">'
        f'{crumb}<h1>{title}</h1>{lead}{extra}</div>'
        f'<p class="photo-credit"><a href="{url}">{e(name)} · Carol M. Highsmith, Library of Congress</a></p></section>'
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


def site_config():
    """Optional owner settings (content/site.json): search-console verification tokens."""
    try:
        return json.loads((ROOT / 'content/site.json').read_text())
    except FileNotFoundError:
        return {}


# path -> last-modified date (ISO), filled by page() and read by the sitemap builder
LASTMOD = {}
ORG_ID = SITE + '/#organization'
ROBOTS = 'index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1'


def schema_graph(title, desc, path, kind, home, *, image, published, modified, breadcrumbs, extra):
    url = SITE + path
    organization = {
        '@type': 'Organization', '@id': ORG_ID, 'name': 'Maryland Eagles Eyes', 'alternateName': 'MD Eagles',
        'url': SITE + '/', 'logo': {'@type': 'ImageObject', 'url': SITE + '/assets/icon-512.png', 'width': 512, 'height': 512},
        'description': 'An independent publication about problems facing people in Maryland, with possible solutions, '
                       'and guides to the help that already exists.',
        'areaServed': {'@type': 'AdministrativeArea', 'name': 'Maryland'},
        'sameAs': ['https://buttondown.com/eagles'],
    }
    page_node = {'@type': kind, '@id': url + '#webpage', 'name': title, 'description': desc, 'url': url,
                 'inLanguage': 'en-US', 'isPartOf': {'@id': SITE + '/#website'},
                 'primaryImageOfPage': {'@type': 'ImageObject', 'url': image, 'width': 1200, 'height': 630}}
    if modified:
        page_node['dateModified'] = modified
    if kind == 'AboutPage':
        page_node['about'] = {'@id': ORG_ID}
    graph = [organization]
    if home:
        graph.insert(0, {'@type': 'WebSite', '@id': SITE + '/#website', 'name': 'Maryland Eagles Eyes',
                         'alternateName': 'MD Eagles', 'url': SITE + '/', 'inLanguage': 'en-US',
                         'publisher': {'@id': ORG_ID}})
    else:
        graph.append({'@type': 'WebSite', '@id': SITE + '/#website', 'name': 'Maryland Eagles Eyes', 'url': SITE + '/'})
    graph.append(page_node)
    if breadcrumbs:
        trail = [('Home', '/')] + list(breadcrumbs)
        graph.append({'@type': 'BreadcrumbList', '@id': url + '#breadcrumb', 'itemListElement': [
            {'@type': 'ListItem', 'position': n, 'name': name, 'item': SITE + href} for n, (name, href) in enumerate(trail, 1)]})
        page_node['breadcrumb'] = {'@id': url + '#breadcrumb'}
    for node in extra:
        node = dict(node)
        if node.get('@type') == 'Article':
            node.update({'@id': url + '#article', 'mainEntityOfPage': {'@id': url + '#webpage'}, 'url': url,
                         'inLanguage': 'en-US', 'image': [image], 'author': {'@id': ORG_ID}, 'publisher': {'@id': ORG_ID},
                         'datePublished': published or modified, 'dateModified': modified or published,
                         'spatialCoverage': {'@type': 'AdministrativeArea', 'name': 'Maryland'}})
        graph.append(node)
    return json.dumps({'@context': 'https://schema.org', '@graph': graph}, ensure_ascii=False, separators=(',', ':'))


def item_list(name, items):
    """ItemList node for an index page: items are (name, path) pairs."""
    return {'@type': 'ItemList', 'name': name, 'numberOfItems': len(items), 'itemListElement': [
        {'@type': 'ListItem', 'position': n, 'name': item, 'url': SITE + href} for n, (item, href) in enumerate(items, 1)]}


def page(title, desc, path, body, *, current=None, body_class='', scripts=(), kind='WebPage',
         home=False, dialog=False, noindex=False, seo_title=None, image=None, image_alt=None,
         og_type='website', published=None, modified=None, breadcrumbs=(), extra=()):
    """seo_title is the full <title> (<= 65 characters) when the short page name is not the right search title."""
    full_title = seo_title or f'{title} | MD Eagles'
    image_url = SITE + (image or '/assets/social-mdeagles.jpg')
    image_alt = image_alt or 'MD Eagles: Maryland problems with possible solutions, and the help that already exists.'
    if not noindex:
        LASTMOD[path] = modified or LASTMOD.get(path)
    config = site_config()
    verify = ''.join(f'<meta name="{name}" content="{e(config[key])}">' for key, name in (
        ('google_site_verification', 'google-site-verification'), ('bing_site_verification', 'msvalidate.01')) if config.get(key))
    article = ''.join(
        f'<meta property="article:{name}" content="{value}">' for name, value in (
            ('published_time', published), ('modified_time', modified)) if value) if og_type == 'article' else ''
    script_tags = ''.join(f'<script src="{src}" defer></script>' for src in ('/site.js',) + tuple(scripts))
    head = (
        '<!DOCTYPE html><html lang="en-US"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width, initial-scale=1">'
        '<meta name="theme-color" content="#231f20">'
        f'<title>{e(full_title)}</title><meta name="description" content="{e(desc)}">'
        f'<link rel="canonical" href="{SITE}{path}">'
        + ('<meta name="robots" content="noindex">' if noindex else f'<meta name="robots" content="{ROBOTS}">') + verify +
        f'<meta property="og:site_name" content="Maryland Eagles Eyes"><meta property="og:locale" content="en_US">'
        f'<meta property="og:title" content="{e(full_title)}"><meta property="og:description" content="{e(desc)}">'
        f'<meta property="og:url" content="{SITE}{path}"><meta property="og:type" content="{og_type}">{article}'
        f'<meta property="og:image" content="{image_url}"><meta property="og:image:type" content="image/jpeg">'
        f'<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">'
        f'<meta property="og:image:alt" content="{e(image_alt)}">'
        '<meta name="twitter:card" content="summary_large_image">'
        f'<meta name="twitter:title" content="{e(full_title)}"><meta name="twitter:description" content="{e(desc)}">'
        f'<meta name="twitter:image" content="{image_url}"><meta name="twitter:image:alt" content="{e(image_alt)}">'
        f'<link rel="icon" href="/favicon.ico?v={ICON_VERSION}" sizes="48x48">'
        f'<link rel="icon" href="/assets/favicon.svg?v={ICON_VERSION}" type="image/svg+xml">'
        f'<link rel="apple-touch-icon" href="/assets/apple-touch-icon.png?v={ICON_VERSION}">'
        f'<link rel="manifest" href="/site.webmanifest?v={ICON_VERSION}">'
        '<link rel="preload" href="/assets/newsreader.woff2" as="font" type="font/woff2" crossorigin>'
        '<link rel="preload" href="/assets/hanken-grotesk.woff2" as="font" type="font/woff2" crossorigin>'
        '<link rel="stylesheet" href="/style.css">'
        '<script type="application/ld+json">'
        + schema_graph(title, desc, path, kind, home, image=image_url, published=published, modified=modified,
                       breadcrumbs=breadcrumbs, extra=extra) + '</script></head>'
    )
    classes = f' class="{body_class}"' if body_class else ''
    return (
        f'{head}<body{classes}><a class="skip-link" href="#main">Skip to content</a>'
        f'{masthead(current)}<main id="main">{body}</main>{footer()}'
        f'{subscribe_dialog() if dialog else ""}{script_tags}</body></html>'
    )
