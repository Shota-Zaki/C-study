#!/usr/bin/env python3
from pathlib import Path
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import json
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
COURSE = json.loads((ROOT / 'content/course.json').read_text(encoding='utf-8'))
PROJECTS = json.loads((ROOT / 'content/projects.json').read_text(encoding='utf-8'))
CHECKS = []


def check(name, condition, detail=''):
    CHECKS.append((name, bool(condition), str(detail)))


def flatten_keys(value):
    keys = []
    if isinstance(value, dict):
        for key, item in value.items():
            keys.append(str(key))
            keys.extend(flatten_keys(item))
    elif isinstance(value, list):
        for item in value:
            keys.extend(flatten_keys(item))
    return keys


# ---------------------------------------------------------------------------
# Curriculum invariants
# ---------------------------------------------------------------------------
lessons = COURSE['lessons']
chapters = COURSE['chapters']
check('curriculum: 8 chapters', len(chapters) == 8, len(chapters))
check('curriculum: 32 lessons', len(lessons) == 32, len(lessons))
check('curriculum: lesson ids 01..32', [l['id'] for l in lessons] == [f'{i:02d}' for i in range(1, 33)])
check('curriculum: chapter ids 1..8', [c['id'] for c in chapters] == list(range(1, 9)))
check('curriculum: 4 lessons per chapter', all(sum(1 for l in lessons if l['chapter'] == cid) == 4 for cid in range(1, 9)))
check('curriculum: lesson chapter order', all(l['chapter'] == ((idx - 1) // 4 + 1) for idx, l in enumerate(lessons, 1)))
check('curriculum: 5 questions per lesson', all(len(l['questions']) == 5 for l in lessons))
check('curriculum: 160 questions', sum(len(l['questions']) for l in lessons) == 160)
check('curriculum: 4 options per question', all(len(q['options']) == 4 for l in lessons for q in l['questions']))
check('curriculum: 4 explanations per question', all(len(q['reasons']) == 4 for l in lessons for q in l['questions']))
check('curriculum: 640 options', sum(len(q['options']) for l in lessons for q in l['questions']) == 640)
check('curriculum: 640 option explanations', sum(len(q['reasons']) for l in lessons for q in l['questions']) == 640)
check('curriculum: answer indices valid', all(isinstance(q.get('answer'), int) and 0 <= q['answer'] < 4 for l in lessons for q in l['questions']))
check('curriculum: base exercise every lesson', all(isinstance(l.get('exercise'), dict) and l['exercise'].get('task') and l['exercise'].get('solution') for l in lessons))
check('curriculum: 2 deep drills every lesson', all(len(l['deep']['drills']) == 2 for l in lessons))
check('curriculum: 96 exercises', sum(1 + len(l['deep']['drills']) for l in lessons) == 96)
check('curriculum: 3 production projects', len(PROJECTS) == 3, len(PROJECTS))
check('curriculum: standalone explanation every lesson', all(l.get('csharp_focus', {}).get('point') and l['csharp_focus'].get('why') for l in lessons))
check('curriculum: concepts every lesson', all(l.get('deep', {}).get('concepts') for l in lessons))
check('curriculum: worked flow every lesson', all(l.get('deep', {}).get('walk', {}).get('code') and l['deep']['walk'].get('rows') for l in lessons))
check('curriculum: bug repair every lesson', all(l.get('deep', {}).get('bug', {}).get('before') and l['deep']['bug'].get('after') for l in lessons))

# Legacy comparison-model keys must not survive the migration.
all_keys = [k.lower() for k in flatten_keys(COURSE)]
legacy_key = 'ja' + 'va'
check('content: no legacy language field', legacy_key not in all_keys)
check('content: no comparison field', 'compare' not in all_keys)

# Prior-language comparison residue audit; JavaScript is intentionally retained.
text_suffixes = {'.html', '.json', '.md', '.js', '.cs', '.txt', '.py', '.sh', '.css', '.xml'}
alltext = '\n'.join(
    p.read_text(encoding='utf-8', errors='ignore')
    for p in ROOT.rglob('*')
    if p.is_file() and p.suffix.lower() in text_suffixes
)
redacted = re.sub(r'JavaScript', '', alltext, flags=re.I)
forbidden = 'Ja' + 'va'
tokens = [
    forbidden, 'J' + 'VM', 'J' + 'RE', 'J' + 'DK', 'ja' + 'vac', 'Ma' + 'ven', 'Gra' + 'dle',
    'Completable' + 'Future', 'try-with-' + 'resources', 'package-' + 'private', 'Array' + 'List',
    'Hash' + 'Map', 'J' + 'Unit', 'Big' + 'Decimal', 'List<' + 'Integer>', 'import' + '相当',
    'package' + 'に近い', 'checked ' + 'exception', 'Silver' + '経験', '既習' + '言語との比較'
]
banned = [t for t in tokens if re.search(re.escape(t), redacted, flags=re.I)]
check('content: no prior-language comparison residue', not banned, ','.join(sorted(set(banned)))[:240])
check('content: JavaScript retained', 'JavaScript' in alltext)

# Known issue guards from the handoff.
check('regression L16: escaped newline', 'StringReader("C#\\n.NET")' in lessons[15]['example'])
check('regression L21: JSON quotes escaped', '{\\"Title\\":\\"C#\\"' in lessons[20]['deep']['walk']['code'])
check('regression L28: JSON quotes escaped', '{\\"Value\\":80}' in lessons[27]['deep']['walk']['code'])

# ---------------------------------------------------------------------------
# HTML, navigation, SEO, semantics, and local links
# ---------------------------------------------------------------------------
htmls = sorted(ROOT.rglob('*.html'))
check('site: index.html exists', (ROOT / 'index.html').is_file())
check('site: 404.html exists', (ROOT / '404.html').is_file())
check('site: settings.html exists', (ROOT / 'settings.html').is_file())
check('site: 32 lesson pages exist', all((ROOT / 'lessons' / f'{i:02d}.html').is_file() for i in range(1, 33)))
check('site: 3 project pages exist', all((ROOT / 'projects' / f'{name}.html').is_file() for name in ('expense-cli', 'task-cli', 'task-api')))
check('site: robots.txt exists', (ROOT / 'robots.txt').is_file())

# Packaged C# sample inventory and command targets.
csprojs = sorted((ROOT / 'samples').rglob('*.csproj'))
csfiles = sorted((ROOT / 'samples').rglob('Program.cs'))
check('samples: 35 projects', len(csprojs) == 35, len(csprojs))
check('samples: 35 Program.cs files', len(csfiles) == 35, len(csfiles))
check('samples: all target net10.0', all('<TargetFramework>net10.0</TargetFramework>' in p.read_text(encoding='utf-8') for p in csprojs))
check('samples: lesson Program.cs matches course examples', all((ROOT / 'samples' / 'lessons' / f"lesson-{lesson['id']}" / 'Program.cs').read_text(encoding='utf-8').strip() == lesson['example'].strip() for lesson in lessons))
check('samples: project Program.cs matches project examples', all((ROOT / 'samples' / 'projects' / project['id'] / 'Program.cs').read_text(encoding='utf-8').strip() == project['code'].strip() for project in PROJECTS))
sample_targets = sorted(set(re.findall(r'dotnet run --project (samples/[^\s\\"<]+)', alltext)))
check('samples: packaged command targets exist', all((ROOT / target).exists() for target in sample_targets), sample_targets)

broken = []
external_urls = set()
for f in htmls:
    rel = f.relative_to(ROOT)
    soup = BeautifulSoup(f.read_text(encoding='utf-8'), 'html.parser')
    check(f'html {rel}: lang=ja', soup.html is not None and soup.html.get('lang') == 'ja')
    check(f'html {rel}: one h1', len(soup.find_all('h1')) == 1, len(soup.find_all('h1')))
    check(f'html {rel}: main', soup.find('main') is not None)
    check(f'html {rel}: title', bool(soup.title and soup.title.get_text(strip=True)))
    check(f'html {rel}: description', bool(soup.find('meta', attrs={'name': 'description', 'content': True})))
    check(f'html {rel}: viewport', bool(soup.find('meta', attrs={'name': 'viewport'})))
    check(f'html {rel}: canonical', bool(soup.find('link', attrs={'rel': lambda x: x and 'canonical' in x, 'href': True})))
    check(f'html {rel}: skip link', bool(soup.find('a', class_='skip-link', href='#main')))
    check(f'html {rel}: visible nav landmark', bool(soup.find('nav', attrs={'aria-label': True})))
    check(f'html {rel}: no positive tabindex', not any(int(t.get('tabindex', '0')) > 0 for t in soup.find_all(attrs={'tabindex': True}) if str(t.get('tabindex', '')).lstrip('-').isdigit()))
    for a in soup.find_all('a', href=True):
        href = a['href'].strip()
        if not href or href.startswith(('#', 'mailto:', 'tel:')):
            continue
        if href.startswith(('http://', 'https://')):
            external_urls.add(href)
            continue
        local = href.split('#', 1)[0].split('?', 1)[0]
        target = (f.parent / local).resolve()
        if not target.exists():
            broken.append((str(rel), href))
check('links: all internal targets exist', not broken, broken[:10])
check('links: all external URLs parse', all(urlparse(u).scheme in {'http', 'https'} and urlparse(u).netloc for u in external_urls), len(external_urls))

# Exact lesson page identity and prev/next navigation.
for idx in range(1, 33):
    f = ROOT / 'lessons' / f'{idx:02d}.html'
    soup = BeautifulSoup(f.read_text(encoding='utf-8'), 'html.parser')
    body = soup.body
    check(f'lesson {idx:02d}: body id', body is not None and body.get('data-lesson') == f'{idx:02d}')
    current = soup.select_one('.lesson-link[aria-current="page"]')
    check(f'lesson {idx:02d}: current nav', current is not None and current.get('href', '').endswith(f'{idx:02d}.html'))
    prev_next = soup.select('.prev-next a')
    expected_count = 1 if idx == 1 else 2
    check(f'lesson {idx:02d}: prev/next count', len(prev_next) == expected_count, len(prev_next))
    hrefs = [a.get('href', '') for a in prev_next]
    if idx > 1:
        check(f'lesson {idx:02d}: previous target', any(h.endswith(f'{idx-1:02d}.html') for h in hrefs), hrefs)
    if idx < 32:
        check(f'lesson {idx:02d}: next target', any(h.endswith(f'{idx+1:02d}.html') for h in hrefs), hrefs)
    else:
        check('lesson 32: project continuation', any(h.endswith('../projects/index.html') for h in hrefs), hrefs)
    right_toc = soup.select('.right-toc a')
    compact_toc = soup.select('.compact-toc a')
    check(f'lesson {idx:02d}: desktop page TOC', len(right_toc) >= 5, len(right_toc))
    check(f'lesson {idx:02d}: compact page TOC', len(compact_toc) == len(right_toc) and [a.get('href') for a in compact_toc] == [a.get('href') for a in right_toc], len(compact_toc))
    check(f'lesson {idx:02d}: 5 rendered questions', len(soup.select('.question')) == 5, len(soup.select('.question')))
    check(f'lesson {idx:02d}: 20 rendered explanations', len(soup.select('.choice-explain')) == 20, len(soup.select('.choice-explain')))
    check(f'lesson {idx:02d}: 3 rendered drafts', len(soup.select('textarea.draft')) == 3, len(soup.select('textarea.draft')))
    codeboxes = soup.select('.codebox')
    check(f'lesson {idx:02d}: code labels', bool(codeboxes) and all(box.select_one('.codehead') for box in codeboxes), len(codeboxes))
    check(f'lesson {idx:02d}: copy buttons', bool(codeboxes) and all(box.select_one('.copy-btn') for box in codeboxes), len(codeboxes))

# 404 should not be indexed.
s404 = BeautifulSoup((ROOT / '404.html').read_text(encoding='utf-8'), 'html.parser')
robots_404 = s404.find('meta', attrs={'name': 'robots'})
check('seo: 404 noindex', robots_404 is not None and 'noindex' in robots_404.get('content', '').lower())

# CSS invariants used by responsive/accessible UI. Browser behavior is checked separately.
css = (ROOT / 'assets/css/site.css').read_text(encoding='utf-8')
check('css: body prevents page horizontal overflow', 'body{' in css and 'overflow-x:hidden' in css)
check('css: code scroll is contained', '.codebox pre{' in css and 'overflow:auto' in css)
check('css: table scroll is contained', '.table-scroll{' in css and 'overflow-x:auto' in css)
check('css: desktop 3-column layout', 'grid-template-columns:var(--left) minmax(0,1fr) var(--right)' in css)
check('css: tablet hides right TOC', '@media (max-width:1180px)' in css and '.right-toc{display:none}' in css)
check('css: mobile drawer breakpoint', '@media (max-width:820px)' in css and 'translateX(-105%)' in css and '.left-nav.open{transform:translateX(0)' in css)
check('css: dark theme variables', 'html[data-theme="dark"]' in css)
check('css: reduced motion', '@media (prefers-reduced-motion:reduce)' in css)
check('css: visible focus', ':focus-visible{' in css)

# Learning-state defensive import validation is inspected by source and exercised in browser_audit.py.
js = (ROOT / 'assets/js/site.js').read_text(encoding='utf-8')
check('state: storage namespace', 'cstudy.learning.v2' in js)
check('state: import size limit', 'MAX=524288' in js or '512*1024' in js or '512 * 1024' in js)
check('state: import validation function', 'validate(' in js)
check('state: guarded replacement', 'localStorage.setItem' in js and 'JSON.parse' in js)
check('state: draft-only wording', '下書き' in alltext and 'ブラウザー' in alltext)

failed = [x for x in CHECKS if not x[1]]
print(f'checks={len(CHECKS)} pass={len(CHECKS)-len(failed)} fail={len(failed)}')
for name, ok, detail in failed:
    print('FAIL', name, detail)
raise SystemExit(1 if failed else 0)
