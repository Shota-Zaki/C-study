#!/usr/bin/env python3
from pathlib import Path
from bs4 import BeautifulSoup
import json
import re

ROOT = Path(__file__).resolve().parents[1]
CSS = (ROOT / 'assets/css/site.css').read_text(encoding='utf-8')
failures = []
checks = 0


def check(page, name, condition, detail=''):
    global checks
    checks += 1
    if not condition:
        failures.append({'page': str(page), 'check': name, 'detail': str(detail)})


def has_label(el, soup):
    if el.get('aria-label') or el.get('aria-labelledby'):
        return True
    parent = el.find_parent('label')
    if parent and parent.get_text(' ', strip=True):
        return True
    el_id = el.get('id')
    return bool(el_id and soup.find('label', attrs={'for': el_id}))


def accessible_name(el, soup):
    if el.get('aria-label') or el.get('aria-labelledby'):
        return True
    if el.get_text(' ', strip=True):
        return True
    return has_label(el, soup)


for page in sorted(ROOT.rglob('*.html')):
    rel = page.relative_to(ROOT)
    soup = BeautifulSoup(page.read_text(encoding='utf-8'), 'html.parser')
    main = soup.find('main')
    headings = main.find_all(re.compile('^h[1-6]$')) if main else []
    levels = [int(h.name[1]) for h in headings]
    check(rel, 'main starts with h1', bool(levels) and levels[0] == 1, levels[:8])
    check(rel, 'no heading level jump in main', all(b <= a + 1 for a, b in zip(levels, levels[1:])), levels)
    for idx, el in enumerate(soup.find_all('button')):
        check(rel, f'button {idx} has accessible name', accessible_name(el, soup), str(el)[:180])
    for idx, el in enumerate(soup.find_all('a', href=True)):
        check(rel, f'link {idx} has accessible name', accessible_name(el, soup), str(el)[:180])
    for idx, el in enumerate(soup.find_all(['input', 'textarea', 'select'])):
        if el.name == 'input' and el.get('type') == 'hidden':
            continue
        check(rel, f'control {idx} has accessible name', has_label(el, soup), str(el)[:180])
    for idx, dialog in enumerate(soup.find_all('dialog')):
        check(rel, f'dialog {idx} has accessible name', bool(dialog.get('aria-label') or dialog.get('aria-labelledby')), str(dialog)[:180])

# WCAG relative luminance and representative theme-pair checks.
def rgb(hex_color):
    h = hex_color.lstrip('#')
    if len(h) == 3:
        h = ''.join(ch * 2 for ch in h)
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))


def luminance(hex_color):
    vals = []
    for c in rgb(hex_color):
        s = c / 255.0
        vals.append(s / 12.92 if s <= 0.04045 else ((s + 0.055) / 1.055) ** 2.4)
    return 0.2126 * vals[0] + 0.7152 * vals[1] + 0.0722 * vals[2]


def contrast(fg, bg):
    hi, lo = sorted((luminance(fg), luminance(bg)), reverse=True)
    return (hi + 0.05) / (lo + 0.05)

pairs = {
    'light ink/paper': ('#17212b', '#ffffff', 4.5),
    'light muted/paper': ('#607080', '#ffffff', 4.5),
    'light accent/paper': ('#4f46e5', '#ffffff', 4.5),
    'light accent-ink/accent-2': ('#312e81', '#eef2ff', 4.5),
    'light focus/paper': ('#7c3aed', '#ffffff', 3.0),
    'dark ink/paper': ('#e6edf3', '#111827', 4.5),
    'dark muted/paper': ('#9ba7b4', '#111827', 4.5),
    'dark accent/paper': ('#a5b4fc', '#111827', 4.5),
    'dark accent-ink/accent-2': ('#dbe4ff', '#20254a', 4.5),
    'dark focus/paper': ('#c4b5fd', '#111827', 3.0),
    'brand white/accent': ('#ffffff', '#4f46e5', 4.5),
    'code text/code background': ('#e7edf5', '#101827', 4.5),
    'code header/code background': ('#b8c4d2', '#101827', 4.5),
}
contrast_results = {}
for name, (fg, bg, threshold) in pairs.items():
    ratio = contrast(fg, bg)
    contrast_results[name] = {'ratio': round(ratio, 2), 'threshold': threshold}
    check('theme', name, ratio >= threshold, f'{ratio:.2f} < {threshold}')

check('css', 'focus-visible rule exists', ':focus-visible{' in CSS)
check('css', 'reduced-motion rule exists', '@media (prefers-reduced-motion:reduce)' in CSS)
check('css', 'dark theme exists', 'html[data-theme="dark"]' in CSS)

report = {
    'checks': checks,
    'pass': checks - len(failures),
    'fail': len(failures),
    'contrast': contrast_results,
    'failures': failures,
}
(ROOT / 'docs/a11y_audit.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(f'checks={checks} pass={checks-len(failures)} fail={len(failures)}')
for item in failures[:50]:
    print('FAIL', item)
raise SystemExit(1 if failures else 0)
