"""Tell IndexNow search engines (Bing, Yandex, Naver, Seznam, Yep) that pages changed.

    python3 scripts/indexnow.py            # prints what it would send (dry run)
    python3 scripts/indexnow.py --send     # sends it, after the site is deployed

Run this only AFTER the new pages are live, because the engines fetch them. The key file
(public/<key>.txt) proves ownership and is public by design. Google does not use IndexNow:
for Google, submit the sitemap in Search Console. Uses sitemap.xml, so run `python3 scripts/build.py` first.
"""
import json
import sys
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HOST = 'mdeagles.com'
key = json.loads((ROOT / 'content/indexnow.json').read_text())['key']
ns = {'s': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
urls = [u.text for u in ET.parse(ROOT / 'public/sitemap.xml').findall('s:url/s:loc', ns)]
payload = {'host': HOST, 'key': key, 'keyLocation': f'https://{HOST}/{key}.txt', 'urlList': urls}
print(f'{len(urls)} URLs for {HOST}')
if '--send' not in sys.argv:
    print('Dry run. Add --send to submit.')
    sys.exit(0)
request = urllib.request.Request('https://api.indexnow.org/indexnow', data=json.dumps(payload).encode(),
                                 headers={'Content-Type': 'application/json; charset=utf-8'}, method='POST')
with urllib.request.urlopen(request, timeout=30) as response:
    print('IndexNow responded', response.status)
