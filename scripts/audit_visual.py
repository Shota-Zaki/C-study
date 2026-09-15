#!/usr/bin/env python3
"""Offline structural checks for the visual edition; not a C# runtime test."""
from pathlib import Path
from urllib.parse import urlsplit,unquote
from collections import Counter
from bs4 import BeautifulSoup as BS
import json,sys,xml.etree.ElementTree as ET
R=Path(__file__).resolve().parents[1]
paths=sorted([*R.glob('*.html'),*(R/'lessons').glob('*.html'),*(R/'deep-dives').glob('*.html'),*(R/'guides').glob('*.html'),*(R/'projects').glob('*.html')])
parsed={p:BS(p.read_text(),'html.parser') for p in paths};ids={p:{n.get('id') for n in s.select('[id]')} for p,s in parsed.items()}
errors=[];counts=Counter()
banned=['本編から詳細解説へ','この教材の使い方','仕組みを理解し、書いて確かめる','読むペースは自由','学びを形にする','教材の使い方と手元での検証']
for p,s in parsed.items():
 rel=p.relative_to(R).as_posix();text=s.get_text(' ',strip=True);counts['pages']+=1
 for w in banned:
  if w in text:errors.append(f'{rel}: unwanted copy: {w}')
 allids=[n['id'] for n in s.select('[id]')]
 for id,num in Counter(allids).items():
  if num>1:errors.append(f'{rel}: duplicate id: {id}')
 for tag in s.select('a[href],link[href],script[src],img[src]'):
  val=tag.get('href') or tag.get('src');u=urlsplit(val)
  if u.scheme or u.netloc:continue
  target=(p.parent/unquote(u.path)).resolve() if u.path else p
  if u.path.endswith('/'):target=target/'index.html'
  if not target.exists():errors.append(f'{rel}: missing file: {val}')
  elif u.fragment and target in ids and unquote(u.fragment) not in ids[target]:errors.append(f'{rel}: missing anchor: {val}')
  counts['local_references']+=1
 if s.select_one('.compact-toc'):errors.append(f'{rel}: duplicate article TOC')
 if s.select_one('article .local-terms'):errors.append(f'{rel}: terms remain inside article')
 num=s.body.get('data-current-lesson')
 if num:
  opened=s.select('.chapter-group[open]');expected=(int(num)-1)//4+1
  if len(opened)!=1 or opened[0].get('data-chapter')!=str(expected):errors.append(f'{rel}: current chapter not opened')
  toc=s.select_one('.current-lesson .lesson-toc')
  if not toc:errors.append(f'{rel}: current lesson TOC absent')
  elif [a['href'][1:] for a in toc.select('a')] != [h['id'] for h in s.select('article h2[id]')]:errors.append(f'{rel}: TOC mismatch')
  if not s.select_one('.glossary-rail .term-entry'):errors.append(f'{rel}: term rail absent')
  if len(s.select('article .lesson-diagram'))!=1:errors.append(f'{rel}: diagram absent')
  if len(s.select('article .worked-example'))!=1:errors.append(f'{rel}: added sample absent')
 counts['exercises']+=len(s.select('.exercise'));counts['quiz_questions']+=len(s.select('.question'));counts['code_blocks']+=len(s.select('.codebox'));counts['diagram_placements']+=len(s.select('.lesson-diagram'));counts['additional_example_placements']+=len(s.select('.worked-example'))
 for img in s.select('img'):
  if not img.get('alt'):errors.append(f'{rel}: missing alt')
 for textarea in s.select('textarea[data-draft]'):
  if not textarea.get('id') or not s.select_one(f'label[for="{textarea["id"]}"]'):errors.append(f'{rel}: missing textarea label')
for p in (R/'assets/diagrams').glob('*.svg'):
 try:ET.parse(p)
 except Exception as e:errors.append(f'{p.name}: invalid SVG {e}')
 counts['svg_files']+=1
for key,expected in [('pages',80),('exercises',96),('quiz_questions',160),('diagram_placements',64),('additional_example_placements',64),('svg_files',32)]:
 if counts[key]!=expected:errors.append(f'{key}: {counts[key]} != {expected}')
idx=(R/'assets/js/search-index.js').read_text()
for w in banned:
 if w in idx:errors.append('search index contains '+w)
report={'status':'PASS' if not errors else 'FAIL','counts':dict(counts),'errors':errors,'limits':'Structural checks only. Browser assertions use a separate in-memory rendering harness; C# build/run is not verified.'}
out=R/'validation/visual';out.mkdir(parents=True,exist_ok=True);(out/'structural-audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(report,ensure_ascii=False,indent=2));sys.exit(bool(errors))
