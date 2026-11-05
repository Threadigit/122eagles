"""Validate crawlable metadata, social cards, structured data and the sitemap against the published files.

    python3 tests/seo.py        (run after python3 scripts/build.py)
"""
import json
import re
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit

SITE = 'https://mdeagles.com'
root = Path(__file__).resolve().parents[1] / 'public'


class Page(HTMLParser):
    def __init__(self, source):
        super().__init__()
        self.tags, self.json, self.title = [], [], ''
        self._json = self._title = False
        self.feed(source)

    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        self.tags.append((tag, d))
        self._json = tag == 'script' and d.get('type') == 'application/ld+json'
        self._title = tag == 'title'

    def handle_data(self, data):
        if self._json:
            self.json.append(json.loads(data))
        if self._title:
            self.title += data

    def handle_endtag(self, tag):
        self._json = self._title = False

    def meta(self, key, attr='name'):
        return next((a.get('content', '') for t, a in self.tags if t == 'meta' and a.get(attr) == key), None)

    def types(self):
        return [node.get('@type') for doc in self.json for node in doc['@graph']]


urls, lastmod_expected = [], {}
titles, descriptions = {}, {}
for target in sorted(root.rglob('*.html')):
    file = str(target.relative_to(root))
    path = '/' if file == 'index.html' else '/' + file[:-5]
    page = Page(target.read_text())
    assert sum(t == 'h1' for t, a in page.tags) == 1, f'{file}: exactly one h1'
    assert any(t == 'link' and a.get('rel') == 'canonical' and a.get('href') == SITE + path for t, a in page.tags), f'{file}: canonical'
    assert page.json, f'{file}: JSON-LD'
    for tag, attrs in page.tags:
        for field in ['src', 'href']:
            val = urlsplit(attrs.get(field, '')).path if attrs.get(field, '').startswith('/') else ''
            if val.startswith('/') and not val.startswith('//'):
                local = root / val.lstrip('/')
                assert val == '/' or local.is_file() or local.with_suffix('.html').is_file(), f'{file}: broken link {val}'
    if file == '404.html':
        assert page.meta('robots') == 'noindex'
        continue

    urls.append(SITE + path)
    description = page.meta('description')
    assert 70 <= len(description) <= 165, f'{file}: description is {len(description)} characters'
    assert len(page.title) <= 65, f'{file}: title is {len(page.title)} characters'
    assert page.title not in titles, f'{file}: duplicate title with {titles.get(page.title)}'
    assert description not in descriptions, f'{file}: duplicate description'
    titles[page.title], descriptions[description] = file, file

    robots = page.meta('robots')
    assert 'noindex' not in robots and 'max-image-preview:large' in robots, f'{file}: robots'
    assert page.meta('og:title', 'property') == page.title == page.meta('twitter:title')
    assert page.meta('og:description', 'property') == description
    assert page.meta('og:url', 'property') == SITE + path
    assert page.meta('og:site_name', 'property') and page.meta('og:image:alt', 'property')
    image = page.meta('og:image', 'property')
    assert image.startswith(SITE + '/') and (root / image[len(SITE) + 1:]).is_file(), f'{file}: og:image missing on disk'
    assert page.meta('twitter:image') == image and page.meta('twitter:card') == 'summary_large_image'

    types = page.types()
    assert 'Organization' in types and 'WebSite' in types, f'{file}: Organization and WebSite'
    graph_ids = [node.get('@id') for doc in page.json for node in doc['@graph'] if node.get('@id')]
    assert len(graph_ids) == len(set(graph_ids)), f'{file}: duplicate @id in JSON-LD'
    if path != '/':
        assert 'BreadcrumbList' in types, f'{file}: BreadcrumbList'
    if path.startswith(('/problems/', '/guides/')):
        assert 'Article' in types and page.meta('og:type', 'property') == 'article', f'{file}: Article'
        article = next(n for doc in page.json for n in doc['@graph'] if n.get('@type') == 'Article')
        for field in ('datePublished', 'dateModified'):
            assert re.fullmatch(r'\d{4}-\d{2}-\d{2}', article[field]), f'{file}: {field}'
        assert image.endswith(path.rsplit('/', 1)[1] + '.jpg'), f'{file}: each brief and guide has its own social card'
    if path in ('/problems', '/guides'):
        assert 'ItemList' in types, f'{file}: ItemList'
    lastmod_expected[SITE + path] = True

sitemap = ET.parse(root / 'sitemap.xml')
ns = {'s': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
assert sorted(u.text for u in sitemap.findall('s:url/s:loc', ns)) == sorted(urls)
for url in sitemap.findall('s:url', ns):
    stamp = url.find('s:lastmod', ns)
    assert stamp is not None and re.fullmatch(r'\d{4}-\d{2}-\d{2}', stamp.text), f'{url.find("s:loc", ns).text}: lastmod'

robots_txt = (root / 'robots.txt').read_text()
assert f'Sitemap: {SITE}/sitemap.xml' in robots_txt and 'Disallow: /' not in robots_txt

key = json.loads((root.parent / 'content/indexnow.json').read_text())['key']
assert (root / f'{key}.txt').read_text() == key, 'IndexNow key file must contain the key'

headers = json.loads((root.parent / 'vercel.json').read_text())['headers']
assert any(h['source'] == '/downloads/(.*)' and h['headers'][0]['key'] == 'X-Robots-Tag' for h in headers)
print(f'PASS: {len(urls)} indexable pages: titles, descriptions, social cards, structured data, sitemap lastmod, IndexNow key')
