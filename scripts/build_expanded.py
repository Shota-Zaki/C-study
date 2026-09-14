#!/usr/bin/env python3
"""Build the expanded offline static site. No network or repository changes.
Dependencies: beautifulsoup4, markdown-it-py. Run from any directory.
Input originals are immutable *.template snapshots in content/templates.
"""
from __future__ import annotations
import html,json,re,shutil
from pathlib import Path
from copy import deepcopy
from collections import Counter
from bs4 import BeautifulSoup,NavigableString
from markdown_it import MarkdownIt

ROOT=Path(__file__).resolve().parents[1]
TEMPLATES=ROOT/'content/templates'
MD=MarkdownIt('commonmark',{'html':False}).enable('table')
esc=html.escape

def readj(p):return json.loads(p.read_text(encoding='utf-8'))
def writej(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def soup(s):return BeautifulSoup(s,'html.parser')
def append(parent,markup):
 for n in list(soup(markup).contents):parent.append(n)
def insert_before(node,markup):
 for n in list(soup(markup).contents):node.insert_before(n)
def insert_after(node,markup):
 for n in reversed(list(soup(markup).contents)):node.insert_after(n)

def fence(tokens,idx,options,env):
 t=tokens[idx]; kind=t.info.strip().split(' ')[0] or 'text'; raw=t.content.rstrip('\n')
 if kind in ('flow','memory'):
  lines=[x.strip() for x in raw.splitlines() if x.strip()]
  cells=[]
  for i,line in enumerate(lines,1):
   a,_,b=line.partition('|');cells.append(f'<li><span class="step-number">{i}</span><div><b>{esc(a.strip())}</b><p>{esc(b.strip())}</p></div></li>')
  cap='処理の流れ' if kind=='flow' else '値と参照の関係（概念図。物理的な配置を断定する図ではありません）'
  return f'<figure class="concept-diagram {kind}"><figcaption>{cap}</figcaption><ol>{"".join(cells)}</ol></figure>'
 labels={'csharp':'C# · 独立したコード例','csharp-error':'C# · 失敗を学ぶ例（そのまま起動しない）','csharp-input':'C# · 入力を伴う例','csharp-file':'C# · ファイル操作を伴う例','csharp-web':'C# · Webプロジェクト用','csharp-fragment':'C# · 既存コードへの差分 / 部分例','csharp-test':'C# · テストプロジェクト用','powershell':'ターミナルで入力するコマンド','text':'想定される出力 / データ'}
  # Plain text fences are explanatory, not evidence of actual execution.
 return f'<div class="codebox" data-code-kind="{esc(kind)}"><div class="codehead"><span>{labels.get(kind,esc(kind))}</span><button type="button" class="copy-btn" data-copy>コピー</button></div><pre tabindex="0" aria-label="{esc(labels.get(kind,kind))}"><code class="language-{esc(kind)}">{esc(raw)}</code></pre></div>\n'
MD.renderer.rules['fence']=fence

def render_md(text,prefix='detail'):
 s=soup(MD.render(text));counts=Counter()
 for h in s.select('h2,h3,h4'):
  counts[h.name]+=1;h['id']=f'{prefix}-{h.name}-{counts[h.name]:02d}'
 return s

def group_sections(fragment):
 out=soup('');current=None
 for node in list(fragment.contents):
  if getattr(node,'name',None)=='h2':
   current=out.new_tag('section');current['class']=['detail-section'];out.append(current);current.append(node)
  elif current is not None:current.append(node)
  else:out.append(node)
 return out

course=readj(TEMPLATES/'course-original.json');lessons=course['lessons']
course['version']='4.0.0';course['updated']='2026-09-14';course['edition']='C#単独・詳細解説拡充版'
course['sources'].update(readj(ROOT/'content/verified-sources.json'))
quiz={};coaching={}
for p in sorted((ROOT/'content').glob('quiz_enrichment_*.json')):quiz.update(readj(p))
for p in sorted((ROOT/'content').glob('exercise-coaching-*.json')):coaching.update(readj(p))
glossary=readj(ROOT/'content/glossary-expanded.json');terms=glossary['terms'];term_by_name={x['term']:x for x in terms}
guides=readj(ROOT/'content/guides/meta.json')
for lesson in lessons:
 lid=lesson['id'];assert len(quiz[lid])==5 and len(coaching[lid])==3
 for i,q in enumerate(lesson['questions']):assert len(quiz[lid][i])==4;q['reasonDetails']=quiz[lid][i]
 lesson['exerciseCoaching']=coaching[lid];lesson['deepPage']=f'deep-dives/{lid}.html'
 if lid=='05':
  q=lesson['questions'][1]
  q['prompt']='82点をif / else ifで判定するとき、80点以上より先に60点以上を調べるとどうなる？'
  q['options'][1]='先に一致する >= 60 側へ入り、後続の >= 80 側は調べない'
  q['reasons'][1]='if / else ifは最初にtrueになった分岐を通ります。switch式の包含されたパターンとは異なり、不適切な条件順が必ずコンパイルエラーになるわけではありません。'

extra_refs={'01':['managed','gc','aot'],'07':['params'],'13':['gc','boxing','struct'],'14':['record','equality'],'16':['dispose'],'23':['async'],'24':['cancellation','whenall'],'28':['http-guidelines','http-factory','http-semantics'],'29':['binding','middleware'],'30':['responses','binding','http-semantics'],'31':['asp-di','config','logging'],'32':['integration','middleware','http-semantics']}
def source_box(refs):
 items=[]
 for key in dict.fromkeys(refs):
  if key not in course['sources']:raise ValueError(f'Unknown source: {key}')
  x=course['sources'][key];items.append(f'<li><a href="{esc(x["url"],quote=True)}" target="_blank" rel="noopener noreferrer">{esc(x["title"])}</a></li>')
 return '<section class="source-section"><h2 id="sources">確認に使用した一次情報</h2><p>確認日：2026年9月14日。本文の理解を補うための資料です。学習対象は.NET 10 / C# 14です。パッチ番号は固定しません。</p><ul>'+''.join(items)+'</ul></section>'

STATUS='<aside class="callout verification-note"><strong>コード検証の読み方</strong><p>出力はコードから説明した想定結果です。この制作環境では.NET SDKを利用できず、C#のビルド・実行は未検証です。コード下書きはブラウザーで動作しません。手元で確かめる手順は<a href="../guides/learning-workflow.html">教材の使い方と検証</a>にあります。</p></aside>'

def term_details(t,local=False):
 ident=('local-' if local else '')+t['id']
 caution=f'<p class="term-caution"><b>混同しやすい点：</b>{esc(t["caution"])}</p>' if t.get('caution') else ''
 return f'''<details class="term-entry details" id="{ident}" data-term="{esc(t['term'])}"><summary><b>{esc(t['term'])}</b><span class="term-definition">{esc(t['definition'])}</span></summary><div><dl><dt>役割</dt><dd>{esc(t['role'])}</dd><dt>なぜ必要か</dt><dd>{esc(t['why'])}</dd><dt>具体例</dt><dd>{esc(t['example'])}</dd><dt>つながる学習</dt><dd><a href="../lessons/{t['lesson']}.html">Lesson {t['lesson']} の本編</a> ／ <a href="../deep-dives/{t['lesson']}.html">詳細解説</a></dd></dl>{caution}</div></details>'''

def local_terms(lid):
 selected=[term_by_name[n] for n in glossary['lessonTerms'][lid] if n in term_by_name]
 return '<section class="local-terms"><h2 id="local-terms">このページで押さえる用語</h2><p>まず短い定義を読み、必要に応じて開くと、役割・必要性・具体例を確認できます。本文中の用語リンクも、このページ内の説明につながります。</p>'+''.join(term_details(t,True) for t in selected)+'<p><a href="../guides/glossary.html">180語の用語集で調べる →</a></p></section>'

def bridge(i,deep=False):
 l=lessons[i];prev=lessons[i-1] if i else None;nxt=lessons[i+1] if i+1<len(lessons) else None
 before=f'<a href="../lessons/{prev["id"]}.html">{prev["title"]}</a>：{esc(prev["summary"])}' if prev else '前提となるプログラミング経験は不要です。まず「指示を保存してから動かす」という行動を分けます。'
 after=f'<a href="../lessons/{nxt["id"]}.html">{nxt["title"]}</a>：{esc(nxt["summary"])}' if nxt else '<a href="../projects/index.html">制作課題</a>で、データ・処理・境界・検証を組み合わせます。'
 return f'<section class="learning-bridge"><h2 id="connections">前後の学習とのつながり</h2><dl><dt>ここまで</dt><dd>{before}</dd><dt>今回</dt><dd>{esc(l["summary"])}</dd><dt>次に</dt><dd>{after}</dd></dl></section>'

def new_page(title,description,kind,lid=None):
 s=soup((TEMPLATES/'lessons/01.html.template').read_text());s.title.string=title+' | C# Learning Lab'
 for sel,attr,value in [('meta[name="description"]','content',description),('meta[property="og:title"]','content',title),('meta[property="og:description"]','content',description)]:s.select_one(sel)[attr]=value
 s.select_one('link[rel="canonical"]').decompose();s.body.attrs={'data-base':'../','data-page-kind':kind}
 if lid:s.body['data-deep-lesson']=lid
 a=s.select_one('.article');a.clear()
 append(a,f'<div class="breadcrumb"><a href="../index.html">Home</a> / <a href="../guides/index.html">学習ガイド</a> / {esc(kind)}</div><header class="lesson-head"><div class="eyebrow">C# Learning Lab · {esc(kind)}</div><h1>{esc(title)}</h1><p class="lead">{esc(description)}</p><div class="meta-row"><span class="badge">.NET 10 / C# 14</span><span class="badge">読むペースは自由</span></div></header>')
 for x in s.select('.lesson-link[aria-current]'):del x['aria-current']
 return s

manifest=[]
def extract_samples(md_path,source_url):
 family=md_path.parent.name;slug=md_path.stem;num=0
 for t in MD.parse(md_path.read_text()):
  if t.type!='fence' or not t.info.startswith('csharp'):continue
  num+=1;kind=t.info.strip();folder=Path('samples/expanded')/family/slug/f'example-{num:02d}'
  target=ROOT/folder;target.mkdir(parents=True,exist_ok=True)
  standalone=kind in ('csharp','csharp-input','csharp-file','csharp-web')
  codefile='Program.cs' if standalone else 'Example.cs.txt';(target/codefile).write_text(t.content)
  project=None
  if standalone:
   sdk='Microsoft.NET.Sdk.Web' if kind=='csharp-web' else 'Microsoft.NET.Sdk'
   project=str(folder/'Example.csproj')
   (ROOT/project).write_text(f'<Project Sdk="{sdk}"><PropertyGroup><OutputType>Exe</OutputType><TargetFramework>net10.0</TargetFramework><ImplicitUsings>enable</ImplicitUsings><Nullable>enable</Nullable><LangVersion>14.0</LangVersion></PropertyGroup></Project>\n')
  manifest.append({'id':f'{family}-{slug}-{num:02d}','source':str(md_path.relative_to(ROOT)),'page':source_url,'kind':kind,'code':str(folder/codefile),'project':project,'build':'UNVERIFIED' if standalone else 'NOT_STANDALONE','run':'UNVERIFIED' if standalone else 'NOT_APPLICABLE','autoRun':False,'note':'内容と環境を確認して手元で検証。失敗例・部分例は単独起動しない。'})

# Restore the current originals before each deterministic build.
for p in TEMPLATES.rglob('*.html.template'):
 rel=Path(str(p.relative_to(TEMPLATES))[:-9]);dest=ROOT/rel;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_text(p.read_text())

for i,l in enumerate(lessons):
 lid=l['id'];p=ROOT/'lessons'/f'{lid}.html';s=soup(p.read_text());a=s.select_one('.article')
 for b in s.select('.badge'):
  if '目安' in b.get_text():b.string='読むペースは自由'
 for j,q in enumerate(s.select('.question')):
  q.select_one('legend').string=f'Q{j+1}. '+l['questions'][j]['prompt']
  for k,label in enumerate(q.select('.choice span')):label.string=l['questions'][j]['options'][k]
  for k,e in enumerate(q.select('.choice-explain')):
   e.clear();append(e,('<strong>正解：</strong>' if k==l['questions'][j]['answer'] else '<strong>解説：</strong>')+esc(l['questions'][j]['reasons'][k])+'<p class="reason-detail">'+esc(quiz[lid][j][k])+'</p>')
 for j,e in enumerate(s.select('.exercise')):
  e['id']=f'exercise-{j+1}';c=coaching[lid][j]
  label=e.select_one('.draft-label')
  insert_before(label,f'<div class="exercise-input"><h4>入力例・前提条件</h4><p>{esc(c["input"])}</p></div><details class="details"><summary>考え方のヒント</summary><div><p>{esc(c["hint"])}</p></div></details>')
  answer=e.select('details')[-1];box=answer.select_one(':scope > div')
  append(box,f'<h4>処理と結果の読み解き</h4><p>{esc(c["explanation"])}</p><h4>よくある別解と選び方</h4><p>{esc(c["alternative"])}</p><h4>よくある間違いと確認箇所</h4><p>{esc(c["mistake"])}</p>')
  append(e,f'<p class="practice-transfer"><b>実務へのつながり：</b>{esc(c["transfer"])}</p>')
  if j==0:
   for th in answer.select('th'):
    if th.get_text(strip=True)=='入力 / 条件':th.string='解答で確認する条件'
    elif th.get_text(strip=True)=='期待結果':th.string='確認方法'
   for td in answer.select('td'):
    if td.get_text(strip=True)=='確認':td.string='コードと想定結果を照合'
 # Preview two complete concept sections, preserving all original content.
 text=(ROOT/'content/deep'/f'{lid}.md').read_text();sections=group_sections(render_md(text,'preview'))
 excerpt=''.join(str(x) for x in sections.find_all('section',recursive=False)[:2])
 route=f'<section class="route-card"><h2 id="study-route">本編から詳細解説へ</h2><p>① 本編で概念と最小例をつかむ → ② 詳細ページで仕組み・処理順・失敗例を追う → ③ 三段階の演習で書く → ④ 確認問題の全選択肢を読み直す。</p><a class="detail-link" href="../deep-dives/{lid}.html">Lesson {lid} の詳細解説を開く →</a><p>値・状態の変化、追加のコード例、修正理由、理解の境界をまとめて学べます。</p></section>'
 anchor=s.select_one('#concepts');insert_before(anchor,route+bridge(i)+local_terms(lid))
 insert_after(s.select_one('#concepts'),'<section class="expanded-preview"><h2 id="deeper-concepts">概念をもう一段掘り下げる</h2>'+excerpt+f'<p><a class="detail-link" href="../deep-dives/{lid}.html">続き：処理順・状態変化・修正例を読む →</a></p></section>')
 insert_before(s.select_one('.prev-next'),source_box(l['refs']+extra_refs.get(lid,[])))
 insert_after(s.select_one('.lesson-head'),STATUS)
 p.write_text(str(s))
 # Full cohesive detailed lesson.
 d=new_page(f'{lid} {l["title"]} — 詳細解説',l['summary'],'詳細解説',lid);a=d.select_one('.article')
 append(a,f'<p class="route-card"><a href="../lessons/{lid}.html">← Lesson {lid} の本編</a> ／ <a href="../lessons/{lid}.html#exercises">三段階の演習</a> ／ <a href="../lessons/{lid}.html#quiz">確認問題</a></p>'+STATUS+bridge(i,True)+local_terms(lid))
 append(a,str(group_sections(render_md(text))))
 append(a,f'<section><h2 id="apply">自分でコードを書く</h2><p>本文の小さな実験を終えたら、本編の下書き欄へ進みます。解答を写す前に、入力・必要な状態・出力を自分の言葉で整理してください。</p><div class="practice-links"><a href="../lessons/{lid}.html#exercise-1">基礎演習</a><a href="../lessons/{lid}.html#exercise-2">標準演習</a><a href="../lessons/{lid}.html#exercise-3">応用演習</a></div></section>')
 append(a,source_box(l['refs']+extra_refs.get(lid,[])))
 prev=f'<a href="{lessons[i-1]["id"]}.html">← 前の詳細解説<br>{esc(lessons[i-1]["title"])}</a>' if i else '<a href="../guides/learning-workflow.html">教材の使い方</a>'
 nex=f'<a href="{lessons[i+1]["id"]}.html">次の詳細解説 →<br>{esc(lessons[i+1]["title"])}</a>' if i<31 else '<a href="../projects/index.html">制作課題へ →</a>'
 append(a,f'<nav class="prev-next" aria-label="詳細解説の前後">{prev}{nex}</nav>')
 (ROOT/'deep-dives'/f'{lid}.html').write_text(str(d));extract_samples(ROOT/'content/deep'/f'{lid}.md',f'deep-dives/{lid}.html')

for g in guides:
 s=new_page(g['title'],g['summary'],'補助教材');a=s.select_one('.article');append(a,STATUS)
 append(a,str(group_sections(render_md((ROOT/'content/guides'/f'{g["slug"]}.md').read_text(),'guide'))))
 append(a,source_box(g['refs']));append(a,'<p><a href="index.html">学習ガイド一覧へ →</a></p>')
 (ROOT/'guides'/f'{g["slug"]}.html').write_text(str(s));extract_samples(ROOT/'content/guides'/f'{g["slug"]}.md',f'guides/{g["slug"]}.html')

g=new_page('用語集 — 定義から使いどころへ','定義・役割・必要性・具体例・次に学ぶ場所を180語で整理する。','用語集');a=g.select_one('.article')
append(a,'<label for="term-filter">用語・説明を絞り込む</label><input id="term-filter" class="term-filter" type="search" placeholder="例：参照、非同期、HTTP"><p id="term-count" aria-live="polite">180語</p><p>すべての語に短い定義を表示しています。開くと役割・必要性・具体例・関連レッスンが読めます。絞り込みは表示だけを変え、データを削除しません。</p>')
for ch in range(1,9):
 selected=[t for t in terms if (int(t['lesson'])-1)//4+1==ch]
 append(a,f'<section class="term-group"><h2 id="terms-ch-{ch}">第{ch}章につながる用語</h2>'+''.join(term_details(t) for t in selected)+'</section>')
(ROOT/'guides/glossary.html').write_text(str(g))
g=new_page('学習ガイドと詳細解説','迷った場所から戻れる、用語・処理順・エラー・仕組みの学習地図。','学習ガイド');a=g.select_one('.article')
append(a,'<section><h2 id="how">学び方の全体像</h2><p>まず本編を順番に読み、各レッスンの詳細解説で処理と状態を追います。演習で止まった場合は、下の補助教材から原因に合うものを選びます。</p><p><a class="detail-link" href="glossary.html">用語集：180語の定義・役割・具体例 →</a></p></section><section><h2 id="guides">目的から補助教材を選ぶ</h2><div class="home-grid">'+''.join(f'<a class="home-card" href="{x["slug"]}.html"><h3>{esc(x["title"])}</h3><p>{esc(x["summary"])}</p></a>' for x in guides)+'</div></section>')
for ch in course['chapters']:
 ls=[l for l in lessons if l['chapter']==ch['id']]
 append(a,f'<section><h2 id="chapter-{ch["id"]}">第{ch["id"]}章：{esc(ch["title"])}</h2>'+''.join(f'<div class="lesson-map-item"><h3>{l["id"]} {esc(l["title"])}</h3><p>{esc(l["summary"])}</p><a href="../lessons/{l["id"]}.html">本編・演習・問題</a> ／ <a href="../deep-dives/{l["id"]}.html">仕組み・処理順・失敗例の詳細</a></div>' for l in ls)+'</section>')
(ROOT/'guides/index.html').write_text(str(g))

# Home introduction to the new content, without removing prior course cards.
p=ROOT/'index.html';s=soup(p.read_text());a=s.select_one('.article');anchor=s.select_one('.lesson-head')
intro='<section class="route-card"><h2 id="expanded-learning">仕組みを理解し、書いて確かめる</h2><p>8章・32レッスンの本編に、32の詳細解説、7つの補助教材、180語の用語集を加えました。96の三段階演習と160問の確認問題を、入力条件・処理順・状態変化・失敗の原因から学べます。</p><div class="practice-links"><a href="guides/learning-workflow.html">学習の始め方</a><a href="guides/index.html">詳細解説・ガイド一覧</a><a href="guides/glossary.html">用語集</a></div><p>コードの出力は想定結果です。制作環境での.NETビルド・実行は未検証です。演習欄は下書きとして使い、手元の.NET SDKで確認します。</p></section>'
if anchor:insert_after(anchor,intro)
else: a.insert(0,soup(intro))
p.write_text(str(s))

# Finish every published page: consistent navigation, accessible tables, local definitions, TOC.
search=[];published=[]
for p in sorted(ROOT.rglob('*.html')):
 if p.relative_to(ROOT).parts[0] in ('content','docs','samples'):continue
 rel=p.relative_to(ROOT);base='../' if len(rel.parts)>1 else '';s=soup(p.read_text());a=s.select_one('.article');s.body['data-base']=base
 append(s.head,f'<link rel="stylesheet" href="{base}assets/css/expanded.css">')
 append(s.body,f'<script src="{base}assets/js/expanded.js" defer></script>')
 footer=s.select_one('.nav-footer')
 if footer:
  append(footer,f'<p class="supplement-nav"><a href="{base}guides/index.html">詳細解説・学習ガイド</a><a href="{base}guides/glossary.html">用語集</a><a href="{base}guides/errors.html">エラーの調べ方</a></p>')
 lid=s.body.get('data-lesson') or s.body.get('data-deep-lesson')
 if lid:
  s.body['data-current-lesson']=lid
  for x in s.select('.lesson-link'):
   if x.get('href','').endswith(f'lessons/{lid}.html') or x.get('href','')==f'{lid}.html':x['aria-current']='page'
  # At first prose occurrence, link selected terms to their definition on this page.
  selected=[term_by_name[n] for n in glossary['lessonTerms'][lid] if n in term_by_name]
  done=set()
  for txt in list(a.find_all(string=True)):
   if any(getattr(pa,'name',None) in ('a','code','pre','script','style','summary','h1','h2','h3','h4','button','label') or (getattr(pa,'attrs',None) and ('term-entry' in pa.get('class',[]) or 'local-terms' in pa.get('class',[]))) for pa in txt.parents):continue
   if len(str(txt))<4:continue
   fragments=[str(txt)]
   for t in sorted(selected,key=lambda z:len(z['term']),reverse=True):
    name=t['term']
    if name in done:continue
    pattern=r'(?<![A-Za-z0-9_])'+re.escape(name)+r'(?![A-Za-z0-9_])' if re.search('[A-Za-z]',name) else re.escape(name)
    for n,f in enumerate(fragments):
     if not isinstance(f,str):continue
     m=re.search(pattern,f)
     if not m:continue
     link=s.new_tag('a',href='#local-'+t['id']);link['class']=['term-link'];link['title']=t['definition'];link.string=m.group()
     fragments[n:n+1]=[f[:m.start()],link,f[m.end():]];done.add(name);break
   if len(fragments)>1:
    for f in fragments:txt.insert_before(NavigableString(f) if isinstance(f,str) else f)
    txt.extract()
 # Normalize tables and independently scrollable code blocks.
 for tb in s.select('.article table'):
  if 'table-scroll' not in tb.parent.get('class',[]):wrap=s.new_tag('div');wrap['class']=['table-scroll'];tb.wrap(wrap)
  tb.parent['tabindex']='0';tb.parent['role']='region';tb.parent['aria-label']='比較・状態表。横に収まらない場合はこの枠内をスクロールできます'
  for th in tb.select('thead th'):th['scope']='col'
 for box in s.select('.codebox'):
  pre=box.select_one('pre')
  if pre:pre['tabindex']='0';pre['aria-label']='コード例。必要に応じて枠内を横スクロールできます'
  head=box.select_one('.codehead')
  if head and not head.select_one('[data-wrap-code]'):append(head,'<button type="button" class="copy-btn" data-wrap-code aria-pressed="false">折り返し</button>')
 # Build complete TOCs after content insertions. Header ids cannot duplicate any other element.
 seen=set();h2s=[]
 for el in s.select('[id]'):
  ident=el['id']
  if ident in seen:
   n=2
   while f'{ident}-{n}' in seen:n+=1
   el['id']=f'{ident}-{n}'
  seen.add(el['id'])
 for idx,h in enumerate(a.select('h2'),1):
  if not h.get('id'):h['id']=f'page-section-{idx}'
  h2s.append(h)
 links=''.join(f'<a href="#{h["id"]}">{esc(h.get_text(" ",strip=True))}</a>' for h in h2s)
 compact=s.select_one('.compact-toc')
 if compact:compact.decompose()
 newtoc=soup('<details class="compact-toc"><summary>このページの目次</summary><nav aria-label="ページ内目次">'+links+'</nav></details>').details
 header=a.select_one('.lesson-head')
 if header:header.insert_after(newtoc)
 else:a.insert(0,newtoc)
 right=s.select_one('.right-toc')
 if right:right.clear();append(right,'<h2>このページの目次</h2><nav aria-label="詳細なページ内目次">'+links+'</nav>')
 # Sticky position bar occupies its own grid row, rather than overlaying the article.
 layout=s.select_one('.layout')
 if layout:
  bar=soup('<div class="reading-position" role="navigation" aria-label="現在の読書位置"><a href="#main">先頭</a><span class="reading-title"></span><span data-reading-count></span><button class="position-menu" type="button" data-show-toc>目次</button><span class="reading-track" aria-hidden="true"><span data-reading-progress></span></span></div>').div
  title=s.select_one('h1');bar.select_one('.reading-title').string=title.get_text(' ',strip=True) if title else '本文';layout.insert(0,bar)
 append(s.body,'<p class="storage-warning" role="status" aria-live="polite" hidden data-storage-warning></p>')
 # Native summary details and inputs have visible labels from the original.
 out='<!doctype html>\n'+str(s).replace('<!DOCTYPE html>','').replace('<!doctype html>','')
 p.write_text(out,encoding='utf-8');published.append(str(rel))
 kind='lesson' if rel.parts[0]=='lessons' else 'detail' if rel.parts[0]=='deep-dives' else 'guide' if rel.parts[0]=='guides' else 'project'
 if p.name not in ('404.html','settings.html'):
  search.append({'title':s.h1.get_text(' ',strip=True) if s.h1 else s.title.get_text(),'text':a.get_text(' ',strip=True),'url':str(rel),'kind':kind,'id':lid or ''})

for p in list((ROOT/'samples/lessons').rglob('*.csproj'))+list((ROOT/'samples/projects').rglob('*.csproj')):
 manifest.append({'id':'original-'+p.parent.name,'source':'content/course.json' if 'lessons' in p.parts else 'content/projects.json','page':None,'kind':'original-project','code':str((p.parent/'Program.cs').relative_to(ROOT)),'project':str(p.relative_to(ROOT)),'build':'UNVERIFIED','run':'UNVERIFIED','autoRun':False,'note':'元教材の独立プロジェクト。今回の実ビルド・実行は未検証。'})
writej(ROOT/'samples/manifest.json',{'target':'.NET 10 / C# 14','status':'UNVERIFIED','reason':'SDKが未導入。公式配布先からのSDK取得も失敗。','entries':manifest})
writej(ROOT/'content/course.json',course)
writej(ROOT/'content/published-pages.json',published)
(ROOT/'assets/js/search-index.js').write_text('window.CSTUDY_SEARCH_INDEX='+json.dumps(search,ensure_ascii=False,separators=(',',':'))+';\n')
print(json.dumps({'published_pages':len(published),'lessons':len(lessons),'detailed_lessons':32,'guides':len(guides),'terms':len(terms),'quiz_option_details':sum(len(r) for qs in quiz.values() for r in qs),'exercise_coaching':sum(map(len,coaching.values())),'samples':len(manifest),'projects':sum(bool(x['project']) for x in manifest)},ensure_ascii=False))
