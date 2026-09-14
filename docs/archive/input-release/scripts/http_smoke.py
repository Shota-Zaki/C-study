#!/usr/bin/env python3
from pathlib import Path
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from urllib.request import urlopen
from urllib.error import HTTPError
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
import functools
import json
import threading

ROOT = Path(__file__).resolve().parents[1]

class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        pass

handler = functools.partial(QuietHandler, directory=str(ROOT))
server = ThreadingHTTPServer(('127.0.0.1', 0), handler)
thread = threading.Thread(target=server.serve_forever, daemon=True)
thread.start()
base = f'http://127.0.0.1:{server.server_port}/'

paths = {'/index.html', '/404.html', '/settings.html', '/robots.txt'}
for page in ROOT.rglob('*.html'):
    rel_url = '/' + page.relative_to(ROOT).as_posix()
    soup = BeautifulSoup(page.read_text(encoding='utf-8'), 'html.parser')
    for tag in soup.find_all(True):
        for attr in ('href', 'src'):
            value = tag.get(attr)
            if not value or value.startswith(('#', 'mailto:', 'tel:', 'data:')):
                continue
            if value.startswith(('http://', 'https://')):
                continue
            absolute = urljoin(base + rel_url.lstrip('/'), value)
            parsed = urlparse(absolute)
            if parsed.netloc == urlparse(base).netloc:
                paths.add(parsed.path)

results = []
failures = []
for path in sorted(paths):
    try:
        with urlopen(base.rstrip('/') + path, timeout=3) as response:
            status = response.status
            response.read(128)
        ok = status == 200
    except Exception as exc:
        ok = False
        status = repr(exc)
    results.append({'path': path, 'status': status, 'ok': ok})
    if not ok:
        failures.append({'path': path, 'status': status})

missing_status = None
try:
    urlopen(base + '__cstudy_missing__.html', timeout=3)
    missing_status = 200
except HTTPError as exc:
    missing_status = exc.code
except Exception as exc:
    missing_status = repr(exc)
if missing_status != 404:
    failures.append({'path': '/__cstudy_missing__.html', 'status': missing_status, 'expected': 404})

report = {
    'resources_checked': len(results),
    'resource_failures': len([x for x in failures if x.get('path') != '/__cstudy_missing__.html']),
    'missing_path_status': missing_status,
    'failures': failures,
    'results': results,
}
(ROOT / 'docs/http_smoke.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
server.shutdown()
server.server_close()
print(f'resources={len(results)} pass={len(results)-len([x for x in failures if x.get("path") != "/__cstudy_missing__.html"])} missing_status={missing_status} fail={len(failures)}')
raise SystemExit(1 if failures else 0)
