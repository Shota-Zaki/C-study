#!/usr/bin/env python3
"""Rebuild the static visual edition from immutable sources (no network required).
Run: python scripts/build_visual.py
The original long-form builder is preserved; this pipeline applies the requested
layout, terminology, copy and example changes in a deterministic second stage.
"""
from __future__ import annotations
from pathlib import Path
import html,json,re,subprocess,sys,zipfile
from bs4 import BeautifulSoup as BS, NavigableString
from pygments import highlight
from pygments.lexers import CSharpLexer, PowerShellLexer, JsonLexer, TextLexer
from pygments.formatters import HtmlFormatter
from visual_components import diagram_svg,diagram_html,case_html
ROOT=Path(__file__).resolve().parents[1]
E=html.escape

def fragment(text):return BS(text,'html.parser')
def append(node,text):
    for x in list(fragment(text).contents):node.append(x)
def before(node,text):
    for x in list(fragment(text).contents):node.insert_before(x)
def after(node,text):
    for x in reversed(list(fragment(text).contents)):node.insert_after(x)
def remove_section(h):
    p=h.find_parent('section')
    if p:p.decompose()
    else:h.decompose()

subprocess.run([sys.executable,str(ROOT/'scripts/build_expanded.py')],cwd=ROOT,check=True)
visual=json.loads((ROOT/'content/visual/lessons.json').read_text())
course=json.loads((ROOT/'content/course.json').read_text())
copy_edits=json.loads((ROOT/'content/visual/copy-edits.json').read_text())
for lesson in course['lessons']:
    for old,new in copy_edits.items():lesson['title']=lesson['title'].replace(old,new)
lessons={x['id']:x for x in course['lessons']}
chapter_titles={1:'C#と.NETの基礎',2:'条件分岐・反復・メソッド',3:'オブジェクト指向',4:'型・コレクション・例外',5:'ラムダ式とLINQ',6:'保存・日時・非同期処理',7:'構成・テスト・HTTP',8:'ASP.NET Core Web API'}
chapter_subs={1:'SDK・Program.cs・型・文字列',2:'if・switch・配列・引数・null',3:'クラス・プロパティ・継承・インターフェイス',4:'値型と参照型・record・ジェネリック・using',5:'デリゲート・抽出・遅延実行・enum',6:'JSON・日時・Task・キャンセル',7:'.csproj・NuGet・自動テスト・責務分離',8:'ルーティング・入力検証・DI・APIのテスト'}
for ch in course['chapters']:
    ch['title']=chapter_titles[ch['id']];ch['subtitle']=chapter_subs[ch['id']]
heading_replacements={
 'C#を0から、仕組みまで理解する。':'C# / .NET 入門',
 '概念をもう一段掘り下げる':'仕組みの補足',
 'このレッスンで学ぶこと':'要点',
 '概念と内部の仕組み':'概念・構文',
 '学習ロードマップ':'章・レッスン一覧',
 'プログラムは「手順を正確に再現するもの」':'プログラムの実行手順',
 '手元に最小の実験場を用意する':'コンソールプロジェクトの準備',
 '手を動かす課題：予測・修正・再確認':'演習：出力予測とコード修正',
 '型があると何を防げるのか':'型による値と操作の制限',
 'varは型をなくさない':'varとコンパイル時の型推論',
 '文字列と数値は、見た目が同じでも別の値':'文字列と数値の違い',
 '条件分岐は「今の状態から、次の処理を選ぶ」':'条件式の評価と分岐先',
 '配列は「同じ型の複数の値を、位置で扱うもの」':'配列の要素・添字・長さ',
 'メソッドは入力・処理・結果に名前を付ける':'メソッドの入力・処理・戻り値',
 'nullは空文字や0ではなく「参照する値がない」':'null・空文字・0の違い',
 'クラスは「関連する状態と操作を、一つの型へまとめる」':'クラスによる状態と操作の定義',
 'カプセル化は「変更してよい道筋を決めること」':'カプセル化と変更経路の制限',
 '継承は「基底型として扱える関係」を表す':'継承と基底型・派生型の関係',
 'インターフェイスは「利用側が必要な操作の契約」':'インターフェイスと実装の契約',
 '値型と参照型は「代入で何がコピーされるか」から学ぶ':'値型・参照型の代入とコピー',
 '「同じ実体」と「同じ内容」は違う問い':'参照の同一性と値の等値性',
 'LINQはループを消す魔法ではない':'ループとLINQの対応',
 'IEnumerableは結果の保管庫とは限らない':'IEnumerableと列挙時の処理',
 '実行中の値を次回へ残す':'ファイルとJSONによるデータ保存',
 '「日時」は一種類の意味ではない':'日付・時刻・瞬間の違い',
 'コード以外に何が必要か':'ソースコードとプロジェクト設定',
 '実務では「その日に取れたもの」だけに依存しない':'依存パッケージのバージョン管理',
 '動くことと正しいことを分ける':'期待値と実際の結果の比較',
 'HTTPは相手へ要求を送り、応答を受ける約束':'HTTPの要求と応答',
 '今度はリクエストを受け取る側を作る':'HTTPリクエストを受け取るAPI',
 '依存を「使う側の中で作る」から分ける':'依存オブジェクトの生成と利用の分離',
 '一つの要求を端から端まで説明する':'APIの要求・処理・応答',
 'ここまでの知識を一本につなぐ':'API実装と各機能の対応',
 '3段階の練習と読み直す場所':'基礎・標準・応用演習',
 '選択基準：何でも同じ仕組みで解決しない':'enum・タプル・拡張メソッドの選択基準',
 '読むときに作る状態表':'変数・処理順の状態表',
 '教材の使い方と手元での検証':'.NET SDKと実行コマンド',
 '教材の使い方と検証':'.NET SDKと実行コマンド',
 '学習の始め方':'.NET SDKと実行コマンド',
 '確認に使用した一次情報':'公式資料',
 'C# Focus':'重要',
}
# Slogans, navigation guidance and promotional copy; teaching sections stay.
remove_headings={'本編から詳細解説へ','この教材の使い方','仕組みを理解し、書いて確かめる','学び方の全体像','この教材で進める学習の一周','次へ進むかを判断する','ブラウザーのページとC#のアプリは別物','コードの種類を見分ける'}

manifest=[]
(ROOT/'assets/diagrams').mkdir(parents=True, exist_ok=True)
for num,v in visual.items():
    (ROOT/f'assets/diagrams/lesson-{num}.svg').write_text(diagram_svg(num,v),encoding='utf-8')
    for kind in ('case','detail'):
        p=ROOT/f'samples/visual/{num}/{kind}';p.mkdir(parents=True,exist_ok=True)
        item=v[kind];(p/'Program.cs').write_text(item['code'].rstrip()+'\n',encoding='utf-8')
        sdk='Microsoft.NET.Sdk.Web' if item.get('kind')=='csharp-web' else 'Microsoft.NET.Sdk'
        (p/'Example.csproj').write_text(f'<Project Sdk="{sdk}">\n  <PropertyGroup>\n    <OutputType>Exe</OutputType>\n    <TargetFramework>net10.0</TargetFramework>\n    <LangVersion>14.0</LangVersion>\n    <ImplicitUsings>enable</ImplicitUsings>\n    <Nullable>enable</Nullable>\n  </PropertyGroup>\n</Project>\n')
        (p/'expected.txt').write_text(item['output'].rstrip()+'\n',encoding='utf-8')
        with zipfile.ZipFile(p/'example.zip','w',compression=zipfile.ZIP_DEFLATED) as z:
            for filename in ('Program.cs','Example.csproj','expected.txt'):
                info=zipfile.ZipInfo(filename,(2026,9,15,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED
                z.writestr(info,(p/filename).read_bytes())
        manifest.append({'lesson':num,'case':kind,'title':item['title'],'path':str(p.relative_to(ROOT)),'kind':item.get('kind','csharp'),'status':'static-reviewed; dotnet build/run not performed'})
(ROOT/'content/visual/sample-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')

paths=sorted([*ROOT.glob('*.html'),*(ROOT/'lessons').glob('*.html'),*(ROOT/'deep-dives').glob('*.html'),*(ROOT/'guides').glob('*.html'),*(ROOT/'projects').glob('*.html')])
pages={}
fmt=HtmlFormatter(nowrap=True)
for path in paths:
    rel=path.relative_to(ROOT).as_posix();s=BS(path.read_text(),'html.parser');a=s.select_one('article')
    if not a:continue
    base=s.body.get('data-base','');num=s.body.get('data-current-lesson');is_detail=rel.startswith('deep-dives/')
    for el in list(s.select('.compact-toc,.verification-note,.learning-bridge,.footer-note')):el.decompose()
    for el in list(s.select('.route-card')):el.decompose()
    for badge in list(s.select('.badge')):
        if '読むペース' in badge.text:badge.decompose()
    for h in list(a.select('h2,h3')):
        if not h.parent:continue
        if h.get_text(strip=True) in remove_headings:remove_section(h)
    # Duplicate "write code" promotion at end of detail pages, actual exercises preserved.
    el=a.select_one('#apply')
    if el and is_detail:remove_section(el)
    # Remove short purely navigational sections; retain any code/table-bearing teaching.
    for h in list(a.select('h2')):
        if h.text.strip() in {'学習の接続','次へつながる理解','次の学習で何が増えるか','次の学習で処理を部品へする','理解の境界と次の接続'}:
            sec=h.find_parent('section')
            if sec and not sec.select('pre,table'):sec.decompose()
    # Rephrase headlines throughout (including cards). No changes inside executable code.
    for text in list(s.find_all(string=True)):
        if text.parent.name in ('script','style','code','pre','textarea'):continue
        if text.find_parent(['code','pre','textarea','script','style']):continue
        val=str(text)
        if val.strip() in heading_replacements:text.replace_with(val.replace(val.strip(),heading_replacements[val.strip()]))
    for ch in s.select('.chapter-card'):
        eyebrow=ch.select_one('.eyebrow')
        m=re.search(r'Chapter\s+(\d)',ch.get_text(' ',strip=True))
        if m:
            ci=int(m[1]);h=ch.find(['h2','h3']);ps=ch.find_all('p')
            if h:h.string=chapter_titles[ci]
            if ps:ps[0].string=chapter_subs[ci]
    # Plain informational descriptions instead of course marketing lines.
    if rel=='index.html':
        a.h1.string='C# / .NET 入門'
        a.select_one('.lead').string='基本文法、オブジェクト指向、LINQ、非同期処理、ASP.NET Core Web API。8章・32レッスン。'
        intro=a.select_one('.eyebrow')
        if intro:intro.string='C# LEARNING LAB'
        after(a.select_one('.lesson-head'),'<div class="course-shortcuts"><a href="lessons/01.html">01 C#と.NET</a><a href="guides/index.html">詳細解説・補足</a><a href="guides/glossary.html">用語集</a></div>')
        # Old runtime explanation nested outside a section in original home snapshot.
        for co in list(a.select('.callout')):
            if '教材サイト自体は静的HTML' in co.text:co.decompose()
    if rel=='guides/learning-workflow.html':
        a.h1.string='.NET SDKと実行コマンド'
        a.select_one('.lead').string='プロジェクトの作成、ビルド、実行とエラーの確認。'
        s.title.string='.NET SDKと実行コマンド | C# Learning Lab'
    elif num:
        v=visual[num]
        # Exact content statement, not a slogan about learning.
        a.select_one('.lead').string=v['diagram']['title']+'。'
        hd=a.select_one('.lesson-head')
        tabs=f'<nav class="lesson-tabs" aria-label="レッスンのページ"><a href="{base}lessons/{num}.html"'+(' aria-current="page"' if not is_detail else '')+'>本文・演習</a><a href="'+base+f'deep-dives/{num}.html"'+(' aria-current="page"' if is_detail else '')+'>詳細解説</a></nav>'
        after(hd,tabs+f'<aside class="key-point"><span>重要</span><strong>{E(v["point"])}</strong></aside>')
        point=a.select_one('.key-point')
        after(point,diagram_html(num,v,base))
        if is_detail:
            target=a.select_one('.source-section') or a.select_one('.prev-next')
            if target:before(target,case_html(num,v,base,True))
            else:append(a,case_html(num,v,base,True))
        else:
            target=a.select_one('#exercises') or a.select_one('#quiz')
            if target:before(target,case_html(num,v,base))
            else:append(a,case_html(num,v,base))
            for exercise in a.select('.exercise'):
                draft=exercise.select_one('textarea[data-draft]')
                if not draft:continue
                label=exercise.select_one('.draft-label')
                if label:label.string='コード下書き'
                if not draft.get_text(strip=True):
                    starter=exercise.select_one('details code')
                    if starter:draft.string=starter.get_text()
                m=exercise.select_one('.draft-meta')
                if m:
                    for el in list(m.find_all('span',recursive=False)):
                        if not el.has_attr('data-draft-status'):el.decompose()
                    append(m,f'<button class="plain-btn draft-download" type="button" data-download-draft="{E(draft.get("id",""))}">.cs保存</button>')
                # No fake compiler/execution button: downloaded code is genuine C#.
            # One concise factual label, rather than repeated site-usage prose.
            exercises=a.select_one('#exercises')
            if exercises:
                h=exercises.find('h2');after(h,'<p class="execution-mode">C#実行環境：.NET 10 SDK</p>')
    # Move terms out of article, preserving local ids/links.
    terms=a.select_one('.local-terms');rail=s.select_one('.right-toc')
    if rail:
        rail.clear();rail['class']=['right-toc','glossary-rail'];rail['aria-label']='用語'
        panel=s.new_tag('details');panel['class']=['glossary-panel'];panel['open']='';panel['id']='page-terms'
        append(panel,'<summary>このページの用語 <span aria-hidden="true">＋</span></summary>')
        if terms:
            for el in list(terms.find_all(['h2','p'],recursive=False)):el.decompose()
            terms['class']=['rail-terms']
            append(panel,'<h2>このページで押さえる用語</h2>');panel.append(terms.extract())
        else:
            append(panel,'<h2>用語・補足</h2><div class="rail-resources"><a href="'+base+'guides/glossary.html">C#用語集 <span>180語</span></a><a href="'+base+'guides/errors.html">コンパイル・実行時エラー</a><a href="'+base+'guides/runtime-memory.html">実行環境とメモリ</a></div>')
        rail.append(panel)
        # Term entry now has a compact definition, with details still available.
        for dt in rail.select('dt'):
            if dt.text=='つながる学習':
                dd=dt.find_next_sibling('dd')
                if dd:dd.decompose()
                dt.decompose()
    # Fix internal links to headings removed or renamed; tables of contents built later.
    for link in list(s.select('a[href]')):
        if 'learning-workflow.html' in link['href'] and ('使い方' in link.text or '学習の始め方' in link.text):link.string='.NET SDKと実行コマンド'
    # Site-wide copy audit, separate from code contents and technical examples.
    for text in list(s.find_all(string=True)):
        if text.find_parent(['pre','code','textarea','script','style']):continue
        value=str(text)
        for old,new in copy_edits.items():value=value.replace(old,new)
        value=re.sub(r'第([1-8])章につながる用語',r'第\1章の用語',value)
        if value!=str(text):text.replace_with(value)
    # Give each heading an id without changing old anchors.
    existing={el.get('id') for el in s.select('[id]')}
    for i,h in enumerate(a.select('h2,h3,h4'),1):
        if not h.get('id'):
            ident=f'section-{i}'
            while ident in existing:ident+='-x'
            h['id']=ident;existing.add(ident)
    # Static token highlighting, preserving textContent byte for byte.
    for code in a.select('.codebox pre code'):
        raw=code.get_text();box=code.find_parent(class_='codebox');kind=box.get('data-code-kind','')
        lang=' '.join(code.get('class',[]))
        if not kind:
            label=box.select_one('.codehead').get_text() if box.select_one('.codehead') else ''
            kind='csharp' if 'C#' in label or 'csharp' in lang else 'text'
        lexer=CSharpLexer(stripnl=False,ensurenl=False) if kind.startswith('csharp') else PowerShellLexer(stripnl=False,ensurenl=False) if kind in ('powershell','bash','shell') else JsonLexer(stripnl=False,ensurenl=False) if kind=='json' else TextLexer(stripnl=False,ensurenl=False)
        marked=highlight(raw,lexer,fmt)
        if not raw.endswith('\n'):marked=marked.removesuffix('\n')
        code.clear()
        for node in list(fragment('<pre>'+marked+'</pre>').pre.contents):code.append(node)
        # Pygments must not change copy/download content.
        if code.get_text()!=raw:raise ValueError(f'Highlight modified code: {rel}')
        code['class']=sorted(set(code.get('class',[])+['syntax-code']))
    # CSS loaded last; nav JS replaces original expanded behavior.
    append(s.head,f'<link rel="stylesheet" href="{base}assets/css/visual.css"/>')
    append(s.body,f'<script defer src="{base}assets/js/visual.js"></script>')
    # Metadata is descriptive, not a second cache of old slogans.
    desc=s.select_one('meta[name="description"]')
    if desc:desc['content']=a.select_one('.lead').get_text(' ',strip=True) if a.select_one('.lead') else a.h1.get_text(' ',strip=True)
    pages[rel]=(s,a,base,num,is_detail)

# Navigation built after the page content is final.
for rel,(s,a,base,num,is_detail) in pages.items():
    nav=s.select_one('.left-nav')
    if nav:
        foot=nav.select_one('.nav-footer');footer=foot.extract() if foot else None
        nav.clear();append(nav,'<button class="plain-btn drawer-close" data-drawer="close" type="button">閉じる</button><div class="nav-heading">LESSONS <span>32</span></div>')
        cur_ch=lessons[num]['chapter'] if num else None
        for ch in course['chapters']:
            ci=ch['id'];grp=s.new_tag('details');grp['class']=['chapter-group'];grp['data-chapter']=str(ci)
            if ci==cur_ch:grp['open']='';grp['class'].append('current-chapter')
            append(grp,f'<summary class="chapter-title"><span class="chapter-number">Chapter {ci:02}</span><span>{E(ch["title"])}</span></summary>')
            for lesson in course['lessons']:
                if lesson['chapter']!=ci:continue
                li=lesson['id'];current=li==num
                item=s.new_tag('div');item['class']=['lesson-item']+(['current-lesson'] if current else [])
                append(item,f'<a class="lesson-link" href="{base}lessons/{li}.html"'+(' aria-current="page"' if current and not is_detail else '')+f'><span class="num">{li}</span><span>{E(lesson["title"])}</span></a>')
                if current:
                    if is_detail:append(item,f'<a class="detail-nav-link" aria-current="page" href="{base}deep-dives/{li}.html">詳細解説</a>')
                    toc=s.new_tag('nav');toc['class']=['lesson-toc'];toc['aria-label']='このページの目次'
                    append(toc,'<div class="toc-label">このページの目次</div>')
                    for h in a.select('h2[id]'):
                        nested=h.find_parent(class_='expanded-preview') and h.get('id')!='deeper-concepts'
                        append(toc,f'<a href="#{E(h["id"])}"'+(' class="sub-section"' if nested else '')+f'>{E(h.get_text(" ",strip=True))}</a>')
                    item.append(toc)
                grp.append(item)
            nav.append(grp)
        if not num:
            toc=s.new_tag('details');toc['class']=['page-nav'];toc['open']=''
            append(toc,'<summary>このページの目次</summary>')
            for h in a.select('h2[id]'):append(toc,f'<a href="#{E(h["id"])}">{E(h.get_text(" ",strip=True))}</a>')
            nav.append(toc)
        if footer:nav.append(footer)
    # Global old copy in cards/links not attached to an exact heading.
    for txt in list(s.find_all(string=True)):
        if txt.find_parent(['code','pre','textarea','script','style']):continue
        val=str(txt)
        for old,new in [('ASP.NET Coreで学びを形にする',chapter_subs[8]),('C#と.NETの全体像から、最初の実行へ',chapter_subs[1]),('クラスから、差し替えられる設計へ',chapter_subs[3]),('実務への橋渡し',chapter_titles[7]),('C#らしい型の使い方',chapter_titles[4])]:val=val.replace(old,new)
        if val!=str(txt):txt.replace_with(val)
    # Former learning bridge anchor refs from old source documents route to valid areas.
    ids={el['id'] for el in s.select('[id]')}
    for link in s.select('a[href^="#"]'):
        target=link['href'][1:]
        if target and target not in ids:
            if target in ('local-terms','connections','study-route','apply'):link['href']='#main'
    (ROOT/rel).write_text(str(s)+'\n',encoding='utf-8')

index=[]
for rel,(s,a,base,num,is_detail) in pages.items():
    if rel in ('404.html','settings.html'):continue
    text=a.get_text(' ',strip=True)
    terms=s.select_one('.rail-terms')
    if terms:text+=' '+terms.get_text(' ',strip=True)
    kind='detail' if is_detail else 'lesson' if num else 'guide' if rel.startswith('guides/') else 'project'
    index.append({'title':a.h1.get_text(' ',strip=True),'text':text,'url':rel,'kind':kind})
(ROOT/'assets/js/search-index.js').write_text('window.CSTUDY_SEARCH_INDEX='+json.dumps(index,ensure_ascii=False,separators=(',',':'))+';\n',encoding='utf-8')
course['version']='5.0.0';course['updated']='2026-09-15';course['edition']='図解・実例版'
course['metrics']['visualDiagrams']=32;course['metrics']['additionalExamples']=64
(ROOT/'content/course.json').write_text(json.dumps(course,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(ROOT/'.nojekyll').write_text('')
print(f'Visual edition: {len(pages)} pages / 32 SVG diagrams / 64 added samples')
