"""Local preview that behaves like the Vercel deployment.

    python3 scripts/serve.py [port]        (default 8012)

Serves public/ with clean URLs (/about -> about.html) and the response headers
from vercel.json, including the Content-Security-Policy, so layout and script
problems show up locally instead of in production.
"""
import json
import sys
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / 'public'
HEADERS = [h for rule in json.loads((ROOT / 'vercel.json').read_text())['headers']
           if rule['source'] == '/(.*)' for h in rule['headers']]


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(PUBLIC), **kwargs)

    def translate_path(self, path):
        resolved = Path(super().translate_path(path))
        clean = not path.split('?')[0].endswith('/') and resolved != PUBLIC
        if clean and not resolved.is_file() and resolved.with_suffix('.html').is_file():
            return str(resolved.with_suffix('.html'))
        return str(resolved)

    def end_headers(self):
        for header in HEADERS:
            self.send_header(header['key'], header['value'])
        self.send_header('Cache-Control', 'no-store')
        super().end_headers()


if __name__ == '__main__':
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8012
    ThreadingHTTPServer(('127.0.0.1', port), Handler).serve_forever()
