#!/usr/bin/env python3
"""Create a sitemap only after the publisher supplies the final absolute site URL."""
import json,sys
from pathlib import Path
from urllib.parse import urlsplit,urljoin
from xml.sax.saxutils import escape
if len(sys.argv)!=2:raise SystemExit('usage: python scripts/generate_sitemap.py https://example.com/c-study/')
base=sys.argv[1];url=urlsplit(base)
if url.scheme not in ('http','https') or not url.netloc or url.query or url.fragment:raise SystemExit('An absolute HTTP(S) site-root URL without a query or fragment is required.')
root=Path(__file__).resolve().parents[1];base=base.rstrip('/')+'/'
pages=json.loads((root/'content/published-pages.json').read_text())
urls=[urljoin(base,p) for p in pages if p not in ('404.html','settings.html')]
xml='<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+''.join('  <url><loc>'+escape(u)+'</loc></url>\n' for u in urls)+'</urlset>\n'
(root/'sitemap.xml').write_text(xml,encoding='utf-8');print('sitemap.xml:',len(urls),'URLs')
