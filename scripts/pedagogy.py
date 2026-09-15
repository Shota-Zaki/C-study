"""Topic-specific editorial layer for v5.1. Data lives in content/pedagogy.
No network, dynamic diagram service, C# execution or persistence changes.
All original concept fragments and code are retained, with stable old anchors.
"""
from __future__ import annotations
from pathlib import Path
import html, json
from bs4 import BeautifulSoup as BS, Tag

ROOT = Path(__file__).resolve().parents[1]
E = html.escape

def parts(markup: str):
    return list(BS(markup, 'html.parser').contents)

def append(node: Tag, markup: str):
    for child in parts(markup): node.append(child)

def after(node: Tag, markup: str):
    for child in reversed(parts(markup)): node.insert_after(child)

def item(label, value, note=''):
    return f'<div class="figure-card"><b>{E(str(label))}</b><code>{E(str(value))}</code>' + (f'<p>{E(str(note))}</p>' if note else '') + '</div>'

def diagram(d: dict) -> str:
    k=d['kind']; body=''
    if k=='flow':
        body='<ol class="diagram-flow">'+''.join(f'<li><span class="flow-number">{i}</span>{item(*step)}</li>' for i,step in enumerate(d['steps'],1))+'</ol>'
    elif k=='compare':
        body='<div class="diagram-compare">'+''.join(item(*x) for x in d['items'])+'</div>'
    elif k=='tokens':
        body='<dl class="diagram-tokens">'+''.join(f'<div><dt><code>{E(code)}</code></dt><dd>{E(mean)}</dd></div>' for code,mean in d['parts'])+'</dl>'
    elif k=='branch':
        body=f'<div class="diagram-branch"><div class="branch-condition"><span>判定</span><code>{E(d["condition"])}</code></div><div class="branch-paths">'+''.join(f'<div class="branch-path"><b class="branch-label">{E(x[0])} ↓</b><p>{E(x[1])}</p></div>' for x in [d['yes'],d['no']])+'</div></div>'
    elif k in ('trace','matrix'):
        body='<div class="diagram-table-scroll" tabindex="0" role="region" aria-label="'+E(d['title'])+'"><table><thead><tr>'+''.join(f'<th scope="col">{E(str(x))}</th>' for x in d['headers'])+'</tr></thead><tbody>'
        for row in d['rows']:
            assert len(row)==len(d['headers']), d['id']
            body+='<tr>'+''.join(f'<{ "th scope=\"row\"" if i==0 else "td"}>{E(str(x))}</{ "th" if i==0 else "td"}>' for i,x in enumerate(row))+'</tr>'
        body+='</tbody></table></div>'
    elif k=='timeline':
        body='<div class="diagram-table-scroll" tabindex="0" role="region" aria-label="'+E(d['title'])+'"><table class="timeline-table"><thead><tr><th scope="col">処理 / 時間 →</th>'+''.join(f'<th scope="col">{E(x)}</th>' for x in d['columns'])+'</tr></thead><tbody>'
        for row in d['rows']:
            assert len(row)==len(d['columns'])+1,d['id']
            body+=f'<tr><th scope="row">{E(row[0])}</th>'+''.join(f'<td><span class="time-event">{E(x)}</span></td>' for x in row[1:])+'</tr>'
        body+='</tbody></table></div>'
    elif k=='memory':
        body='<div class="diagram-memory">'
        for oid,title,value in d['objects']:
            refs=[r for r in d['refs'] if r[1]==oid]
            body+='<div class="memory-relation"><div class="memory-refs">'+''.join(f'<div class="memory-ref"><b>{E(r[0])}</b><small>{E(r[2])}</small><span aria-hidden="true">→</span><span class="sr-only">は{E(title)}を参照する</span></div>' for r in refs)+'</div>'+f'<div class="memory-object"><b>{E(title)}</b><code>{E(value)}</code></div></div>'
        body+='</div><p class="diagram-qualifier">矢印は参照関係を表します。物理的なメモリ位置やアドレスの図ではありません。</p>'
    elif k=='sequence':
        body='<div class="sequence-actors">'+''.join(f'<span>{E(a)}</span>' for a in d['actors'])+'</div><ol class="diagram-sequence">'
        for source,target,message in d['steps']:
            body+=f'<li><span class="sequence-from">{E(source)}</span><span class="sequence-message"><span class="sequence-arrow" aria-hidden="true">→</span>{E(message)}</span><span class="sequence-to">{E(target)}</span></li>'
        body+='</ol>'
    elif k=='boundary':
        body='<div class="diagram-boundary">'+''.join(f'<div><code>{E(x)}</code><p>{E(y)}</p></div>' for x,y in d['points'])+'</div>'
    elif k=='array':
        body='<div class="diagram-array">'+''.join(f'<div><small>添字 {i}</small><code>{E(x)}</code></div>' for i,x in enumerate(d['values']))+f'</div><div class="array-length">← 要素数 Length = {len(d["values"])} →</div>'
    elif k=='loop':
        body=f'<div class="diagram-loop"><div class="loop-start">{E(d["initial"])}</div><div class="loop-down" aria-hidden="true">↓</div><div class="loop-cycle"><div class="loop-condition"><b>条件を判定</b><code>{E(d["condition"])}</code></div><div class="loop-yes">true ↓</div><div class="loop-body">{E(d["body"])}</div><div class="loop-down" aria-hidden="true">↓</div><div class="loop-update">{E(d["update"])}</div><div class="loop-return">↶ 条件の判定へ戻る</div></div><div class="loop-exit"><b>条件がfalse</b><span>→ {E(d["exit"])}</span></div></div>'
    elif k=='stack':
        body='<ol class="diagram-stack">'+''.join(f'<li style="--stack-depth:{i}"><b>{E(a)}</b><span>{E(b)}</span></li>' for i,(a,b) in enumerate(d['frames']))+'</ol><div class="stack-return">戻る順序：一番深い呼び出し → 呼び出した側 → 元の処理</div>'
    else: raise ValueError(f'Unknown diagram kind: {k}')
    return f'<div class="explain-visual" data-diagram-id="{E(d["id"])}"><p class="diagram-intro">{E(d["before"])}</p><figure id="{E(d["id"])}" class="teaching-figure teaching-{k}" aria-labelledby="{E(d["id"])}-caption"><figcaption id="{E(d["id"])}-caption"><span>図解</span><strong>{E(d["title"])}</strong></figcaption><div class="figure-body">{body}</div></figure><p class="diagram-takeaway">{E(d["after"])}</p></div>'

def insert_diagram(a, d):
    selector,*modes=d['target'].split('|')
    target=a.select_one(selector)
    if target is None: raise ValueError(f'Missing diagram target {d["id"]}: {selector}')
    if modes and modes[0]=='code':
        code=target.select_one('.codebox')
        if code is None: raise ValueError(f'No code in target: {d["id"]}')
        after(code,diagram(d));return
    if target.name in ('h2','h3','h4'):
        target=target.find_parent(class_='concept-part') or target.find_parent('section')
    append(target,diagram(d))

def regroup(a, p, n):
    original=a.select_one('#concepts')
    if original is None: raise ValueError(f'Concepts absent: {n}')
    head=original.find('h2',recursive=False)
    chunks={};intro=[];current=None
    for node in list(original.contents):
        if node is head:continue
        if getattr(node,'name',None)=='h3':
            key=int(node['id'].split('-')[1])
            current=BS('<div class="concept-part"></div>','html.parser').div
            chunks[key]=current
        if current is None:intro.append(node.extract())
        else:current.append(node.extract())
    keys=[part for g in p['groups'] for part in g['parts']]
    if sorted(keys)!=sorted(chunks) or len(set(keys))!=len(keys):
        raise ValueError(f'Concept partition mismatch: {n}: {sorted(chunks)} / {keys}')
    # Keep the original #concepts and its h2 anchor on the first group.
    original.clear(); blocks={}
    for i,g in enumerate(p['groups']):
        if i==0:
            section=original;head.string=g['title'];section.append(head)
            for node in intro:section.append(node)
        else:
            section=BS(f'<section id="topic-{n}-{g["key"]}"><h2 id="topic-{n}-{g["key"]}-heading">{E(g["title"])}</h2></section>','html.parser').section
        section['class']=['topic-section']
        for key in g['parts']:section.append(chunks[key])
        blocks[g['key']]=section
    for key,sel in [('example','#example'),('walk','#walk'),('preview','.expanded-preview'),('worked','#worked-case'),('pitfall','#pitfall')]:
        node=a.select_one(sel)
        if node is None: raise ValueError(f'No block: {n} {key}')
        blocks[key]=node
    blocks['example'].find('h2').string=p['example_title']
    blocks['preview'].find('h2').string=p['preview_title']
    walkh=blocks['walk'].find('h3')
    if walkh:
        blocks['walk'].find('h2').string=walkh.get_text(' ',strip=True)
        # Keep deep links to the previous subheading without repeating its text.
        alias=BS('<span class="anchor-alias"></span>','html.parser').span
        if walkh.get('id'):alias['id']=walkh['id']
        walkh.replace_with(alias)
    if set(p['order'])!=set(blocks) or len(p['order'])!=len(blocks):
        raise ValueError(f'Route does not cover all blocks: {n}')
    marker=a.select_one('#exercises')
    for key in p['order']:marker.insert_before(blocks[key].extract())


def apply(s, a, n, detail, base, visual):
    data=json.loads((ROOT/'content/pedagogy/lessons.json').read_text())
    p=data[n]
    # A contextual entry replaces the detached introductory diagram. Existing
    # learning objectives and substantive paragraphs remain in place.
    point=a.select_one('.key-point')
    if point:after(point,f'<p class="unit-entry">{E(p["opening"])}</p>')
    overview=a.select_one('.visual-section')
    overview.extract()
    vh=overview.find('h2');vh.name='h3'
    if detail:
        target=a.select_one('#'+p['deep_overview_after'])
        if target is None:raise ValueError(n+' missing detail overview target')
        vh.string='本文の実例との対応：'+visual['diagram']['title']
        intro=BS('<p></p>','html.parser').p
        intro.string='次の図は本文の実例「'+visual['case']['title']+'」を使った補助例です。この節のコードとは変数や入力値が異なるため、処理の対応に注目します。'
        vh.insert_after(intro)
        target.find_parent('section').append(overview)
        # The added comparison belongs beside the concept it demonstrates, not
        # permanently at the end of every detail page.
        if p.get('detail_case_after'):
            t=a.select_one('#'+p['detail_case_after']).find_parent('section')
            t.insert_after(a.select_one('#worked-detail').extract())
    else:
        regroup(a,p,n)
        example=a.select_one('#worked-case')
        box=example.select_one('.codebox')
        box.insert_after(overview)
        vh.string='このコードの図解：'+visual['diagram']['title']
    for d in p['deep' if detail else 'main']:insert_diagram(a,d)
    append(s.head,f'<link rel="stylesheet" href="{base}assets/css/pedagogy.css"/>')
    a['data-teaching-edition']='5.1'


def apply_supplement(s,a,rel,base):
    f=ROOT/'content/pedagogy/supplements.json'
    if not f.exists():return
    data=json.loads(f.read_text())
    if rel not in data:return
    for d in data[rel]['diagrams']:insert_diagram(a,d)
    append(s.head,f'<link rel="stylesheet" href="{base}assets/css/pedagogy.css"/>')
