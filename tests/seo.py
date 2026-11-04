"""Validate canonical, crawlable metadata and sitemap against published files."""
import json
from pathlib import Path
from html.parser import HTMLParser
import xml.etree.ElementTree as ET
root=Path(__file__).resolve().parents[1]/'public'
class Page(HTMLParser):
 def __init__(self,source):
  super().__init__();self.tags=[];self.json=[];self.in_json=False;self.feed(source)
 def handle_starttag(self,tag,attrs):
  d=dict(attrs);self.tags.append((tag,d))
  if tag=='script' and d.get('type')=='application/ld+json':self.in_json=True
 def handle_data(self,data):
  if self.in_json:self.json.append(json.loads(data))
 def handle_endtag(self,tag):
  if tag=='script':self.in_json=False
urls=[]
for file,path in [('index.html','/'),('about.html','/about')]:
 page=Page((root/file).read_text())
 assert sum(t=='h1' for t,a in page.tags)==1
 assert any(t=='link' and a.get('rel')=='canonical' and a.get('href')=='https://122eagles.com'+path for t,a in page.tags)
 assert any(t=='meta' and a.get('name')=='description' and len(a.get('content',''))>90 for t,a in page.tags)
 assert page.json
 for tag,attrs in page.tags:
  for field in ['src','href']:
   val=attrs.get(field,'').split('#')[0]
   if val.startswith('/') and not val.startswith('//'):
    local=root/val.lstrip('/')
    assert val=='/' or local.is_file() or local.with_suffix('.html').is_file(),val
 urls.append('https://122eagles.com'+path)
sitemap=ET.parse(root/'sitemap.xml');ns={'s':'http://www.sitemaps.org/schemas/sitemap/0.9'}
assert sorted(e.text for e in sitemap.findall('s:url/s:loc',ns))==sorted(urls)
assert 'Sitemap: https://122eagles.com/sitemap.xml' in (root/'robots.txt').read_text()
assert 'Disallow: /' not in (root/'robots.txt').read_text()
print('PASS: crawlable pages, unique canonicals, metadata, JSON-LD, internal links and sitemap')
