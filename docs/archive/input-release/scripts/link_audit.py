#!/usr/bin/env python3
from pathlib import Path
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
internal = []
external = set()
fragments = []
failures = []

for page in sorted(ROOT.rglob('*.html')):
    rel = page.relative_to(ROOT)
    soup = BeautifulSoup(page.read_text(encoding='utf-8'), 'html.parser')
    ids = {tag.get('id') for tag in soup.find_all(id=True)}
    for a in soup.find_all('a', href=True):
        href = a['href'].strip()
        if not href or href.startswith(('mailto:', 'tel:')):
            continue
        if href.startswith(('http://', 'https://')):
            external.add(href)
            parsed = urlparse(href)
            if parsed.scheme not in {'http', 'https'} or not parsed.netloc or ' ' in href:
                failures.append({'page': str(rel), 'href': href, 'reason': 'invalid external URL'})
            continue
        if href.startswith('#'):
            frag = href[1:]
            fragments.append((str(rel), href))
            if frag and frag not in ids:
                failures.append({'page': str(rel), 'href': href, 'reason': 'missing same-page fragment'})
            continue
        path_part, _, frag = href.partition('#')
        path_part = path_part.split('?', 1)[0]
        target = (page.parent / path_part).resolve()
        internal.append((str(rel), href))
        if not target.exists():
            failures.append({'page': str(rel), 'href': href, 'reason': 'missing local target'})
            continue
        if frag and target.suffix.lower() == '.html':
            target_soup = BeautifulSoup(target.read_text(encoding='utf-8'), 'html.parser')
            if target_soup.find(id=frag) is None:
                failures.append({'page': str(rel), 'href': href, 'reason': 'missing target fragment'})

report = {
    'internal_links_checked': len(internal),
    'same_page_fragments_checked': len(fragments),
    'external_unique_urls': len(external),
    'external_urls': sorted(external),
    'external_network_note': 'Network reachability is audited separately from this offline script.',
    'failures': failures,
}
(ROOT / 'docs/link_audit.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(f'internal={len(internal)} fragments={len(fragments)} external_unique={len(external)} fail={len(failures)}')
for item in failures[:50]:
    print('FAIL', item)
raise SystemExit(1 if failures else 0)
