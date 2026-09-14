#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
import json, tempfile, os, sys
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[1]
CSS=ROOT/'assets/css/site.css'
META=ROOT/'assets/js/course-meta.js'
SEARCH=ROOT/'assets/js/search-index.js'
APP=ROOT/'assets/js/site.js'
results=[]

def add(name,ok,detail=''):
    results.append((name,bool(ok),str(detail)))
    if not ok: print('FAIL',name,detail)

def prepared_html(rel:str)->str:
    p=ROOT/rel
    soup=BeautifulSoup(p.read_text(encoding='utf-8'),'html.parser')
    for tag in soup.find_all('script',src=True): tag.decompose()
    for tag in soup.find_all('link',rel=lambda x:x and 'stylesheet' in x): tag.decompose()
    return str(soup)

def install_storage(page, initial=None):
    data=json.dumps(initial or {},ensure_ascii=False)
    page.evaluate(f'''(()=>{{let d={data};Object.defineProperty(window,'localStorage',{{configurable:true,value:{{getItem:k=>Object.prototype.hasOwnProperty.call(d,k)?d[k]:null,setItem:(k,v)=>d[k]=String(v),removeItem:k=>delete d[k],clear:()=>{{d={{}}}}}}}});window.__cstudyStorage=()=>JSON.parse(JSON.stringify(d));}})()''')

def new_page(ctx, rel:str, viewport, initial_storage=None):
    page=ctx.new_page()
    page.set_viewport_size(viewport)
    errs=[]
    page.on('pageerror',lambda exc:errs.append('pageerror: '+str(exc)))
    page.on('console',lambda m:errs.append('console error: '+m.text) if m.type=='error' else None)
    page.set_content(prepared_html(rel),wait_until='load')
    install_storage(page,initial_storage)
    page.add_style_tag(path=str(CSS))
    page.add_script_tag(path=str(META));page.add_script_tag(path=str(SEARCH));page.add_script_tag(path=str(APP))
    page.wait_for_timeout(30)
    return page,errs

def no_overflow(page):
    return page.evaluate('document.documentElement.scrollWidth <= document.documentElement.clientWidth + 1')

def visible(page,sel):
    return page.locator(sel).first.is_visible() if page.locator(sel).count() else False

def stored_state(page):
    raw=page.evaluate("localStorage.getItem('cstudy.learning.v2')")
    return json.loads(raw) if raw else None

with sync_playwright() as p:
    browser=p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox'])
    ctx=browser.new_context(color_scheme='light')

    # Desktop: all 32 lessons.
    for i in range(1,33):
        lid=f'{i:02d}'; rel=f'lessons/{lid}.html'
        page,errs=new_page(ctx,rel,{'width':1440,'height':900})
        add(f'L{lid} page loads',page.locator('body').get_attribute('data-lesson')==lid)
        add(f'L{lid} no JS errors',not errs,' | '.join(errs[:3]))
        add(f'L{lid} one h1',page.locator('h1').count()==1,page.locator('h1').count())
        add(f'L{lid} questions=5',page.locator('.question').count()==5,page.locator('.question').count())
        add(f'L{lid} option explanations=20',page.locator('.choice-explain').count()==20,page.locator('.choice-explain').count())
        add(f'L{lid} drafts=3',page.locator('textarea[data-draft]').count()==3,page.locator('textarea[data-draft]').count())
        add(f'L{lid} desktop no page overflow',no_overflow(page))
        add(f'L{lid} desktop left nav visible',visible(page,'.left-nav'))
        add(f'L{lid} desktop right toc visible',visible(page,'.right-toc'))
        add(f'L{lid} desktop compact toc hidden',not visible(page,'.compact-toc'))
        links=page.locator('.prev-next a'); hrefs=[links.nth(j).get_attribute('href') for j in range(links.count())]
        if i==1:add('L01 next nav',any('02.html' in (h or '') for h in hrefs),hrefs)
        elif i==32:add('L32 prev nav',any('31.html' in (h or '') for h in hrefs),hrefs)
        else:
            add(f'L{lid} prev nav',any(f'{i-1:02d}.html' in (h or '') for h in hrefs),hrefs)
            add(f'L{lid} next nav',any(f'{i+1:02d}.html' in (h or '') for h in hrefs),hrefs)
        good=True
        for j in range(page.locator('.codebox').count()):
            cb=page.locator('.codebox').nth(j)
            if cb.locator('[data-copy]').count()!=1 or cb.locator('.codehead span').count()!=1 or not cb.locator('.codehead span').text_content().strip():good=False;break
        add(f'L{lid} code language/copy',good,f"codeboxes={page.locator('.codebox').count()}")
        page.close()

    # Tablet representative pages.
    for lid in ['01','16','21','28','32']:
        page,errs=new_page(ctx,f'lessons/{lid}.html',{'width':1024,'height':900})
        add(f'L{lid} tablet no overflow',no_overflow(page))
        add(f'L{lid} tablet left nav visible',visible(page,'.left-nav'))
        add(f'L{lid} tablet right toc hidden',not visible(page,'.right-toc'))
        add(f'L{lid} tablet compact toc visible',visible(page,'.compact-toc'))
        add(f'L{lid} tablet no JS errors',not errs,' | '.join(errs[:3]));page.close()

    # Mobile representative pages and drawer behavior.
    for lid in ['01','16','21','28','32']:
        page,errs=new_page(ctx,f'lessons/{lid}.html',{'width':390,'height':844})
        page.wait_for_timeout(220)
        add(f'L{lid} mobile no overflow',no_overflow(page))
        add(f'L{lid} mobile drawer button',visible(page,'[data-drawer="open"]'))
        add(f'L{lid} mobile drawer aria collapsed',page.locator('[data-drawer="open"]').get_attribute('aria-expanded')=='false')
        add(f'L{lid} mobile right toc hidden',not visible(page,'.right-toc'))
        add(f'L{lid} mobile compact toc visible',visible(page,'.compact-toc'))
        add(f'L{lid} mobile nav initially closed',not page.locator('.left-nav').evaluate('(e)=>e.classList.contains("open")'))
        add(f'L{lid} mobile nav initially offscreen',page.locator('.left-nav').evaluate('(e)=>e.getBoundingClientRect().right<=0'))
        page.locator('[data-drawer="open"]').click();page.wait_for_timeout(220);add(f'L{lid} mobile drawer opens',page.locator('.left-nav').evaluate('(e)=>e.classList.contains("open") && e.getBoundingClientRect().left>=-1'))
        add(f'L{lid} mobile drawer aria expanded',page.locator('[data-drawer="open"]').get_attribute('aria-expanded')=='true')
        page.keyboard.press('Escape');page.wait_for_timeout(220)
        add(f'L{lid} mobile drawer Escape closes',not page.locator('.left-nav').evaluate('(e)=>e.classList.contains("open")') and page.locator('[data-drawer="open"]').get_attribute('aria-expanded')=='false')
        page.locator('[data-drawer="open"]').click();page.wait_for_timeout(220)
        page.locator('[data-drawer="close"]').click();page.wait_for_timeout(220);add(f'L{lid} mobile drawer closes',not page.locator('.left-nav').evaluate('(e)=>e.classList.contains("open")') and page.locator('.left-nav').evaluate('(e)=>e.getBoundingClientRect().right<=0'))
        add(f'L{lid} mobile no JS errors',not errs,' | '.join(errs[:3]));page.close()

    # Search behavior.
    page,errs=new_page(ctx,'lessons/01.html',{'width':1440,'height':900})
    page.locator('[data-open-search]').click();add('Search dialog opens',page.locator('#search-dialog').evaluate('(e)=>e.open'))
    page.locator('#search-dialog input').fill('LINQ');page.wait_for_timeout(50)
    add('Search returns LINQ content',page.locator('[data-search-results] a').count()>0 and 'LINQ' in page.locator('[data-search-results]').inner_text())
    page.locator('#search-dialog button').click();add('Search dialog closes',not page.locator('#search-dialog').evaluate('(e)=>e.open'));page.close()

    # Progress / review / draft / quiz persistence.
    page,errs=new_page(ctx,'lessons/01.html',{'width':1440,'height':900})
    page.locator('[data-complete="01"]').click();page.locator('[data-review="01"]').click()
    page.locator('textarea[data-draft="01:base"]').fill('// browser audit draft');page.wait_for_timeout(320)
    for q in page.locator('.question').all():
        ans=int(q.get_attribute('data-answer'));q.locator(f'input[value="{ans}"]').check()
    page.locator('[data-grade]').click();st=stored_state(page)
    add('Quiz result 5/5','5 / 5' in page.locator('[data-quiz-result]').inner_text(),page.locator('[data-quiz-result]').inner_text())
    add('Quiz reveals all 20 explanations',sum(page.locator('.choice-explain').nth(i).is_visible() for i in range(20))==20)
    add('Progress persisted','01' in st['completed']);add('Review persisted','01' in st['review'])
    add('Draft persisted',st['drafts'].get('01:base')=='// browser audit draft',st['drafts'].get('01:base'))
    add('Quiz persisted',st['quiz'].get('01',{}).get('score')==5);page.close()

    # Invalid pre-existing stored state falls back to empty state instead of breaking UI.
    corrupt=json.dumps({'version':2,'theme':'dark','completed':['99'],'review':[],'quiz':{},'drafts':{},'lastLesson':None})
    page,errs=new_page(ctx,'lessons/01.html',{'width':1440,'height':900},{'cstudy.learning.v2':corrupt})
    add('Corrupt stored state falls back safely',not errs and page.locator('[data-progress-text]').first.inner_text().strip()=='0 / 32',' | '.join(errs[:3]));page.close()

    # Settings: themes and JSON import validation.
    page,errs=new_page(ctx,'settings.html',{'width':1440,'height':900})
    sel=page.locator('[data-theme-select]');sel.select_option('dark');page.wait_for_timeout(20);add('Dark mode applies',page.locator('html').get_attribute('data-theme')=='dark')
    sel.select_option('light');page.wait_for_timeout(20);add('Light mode applies',page.locator('html').get_attribute('data-theme')=='light')
    before=page.evaluate("localStorage.getItem('cstudy.learning.v2')")
    with tempfile.TemporaryDirectory() as td:
        td=Path(td)
        with page.expect_download(timeout=5000) as download_info:
            page.locator('[data-export]').click()
        download=download_info.value
        export_path=td/download.suggested_filename
        download.save_as(str(export_path))
        exported=json.loads(export_path.read_text(encoding='utf-8'))
        add('JSON export filename',download.suggested_filename=='cstudy-learning-data.json',download.suggested_filename)
        add('JSON export valid state',exported.get('version')==2 and exported.get('theme')=='light' and isinstance(exported.get('drafts'),dict),exported)
        cases=[]
        (td/'malformed.json').write_text('{ nope',encoding='utf-8');cases.append(('Malformed JSON',td/'malformed.json'))
        bad={'version':2,'updatedAt':'2026-09-14T00:00:00Z','theme':'light','completed':['99'],'review':[],'quiz':{},'drafts':{},'lastLesson':None}
        (td/'bad-id.json').write_text(json.dumps(bad),encoding='utf-8');cases.append(('Invalid lesson id',td/'bad-id.json'))
        bad2={'version':2,'updatedAt':'2026-09-14T00:00:00Z','theme':'light','completed':[],'review':[],'quiz':{},'drafts':{'01:base':123},'lastLesson':None}
        (td/'bad-type.json').write_text(json.dumps(bad2),encoding='utf-8');cases.append(('Invalid draft type',td/'bad-type.json'))
        (td/'oversize.json').write_text('{"x":"'+'a'*530000+'"}',encoding='utf-8');cases.append(('Oversize JSON',td/'oversize.json'))
        for label,path in cases:
            page.locator('[data-import]').set_input_files(str(path));page.wait_for_timeout(80)
            msg=page.locator('[data-import-message]').inner_text();now=page.evaluate("localStorage.getItem('cstudy.learning.v2')")
            add(label+' rejected',msg.startswith('失敗:'),msg);add(label+' preserves data',now==before)
        good={'version':2,'updatedAt':'2026-09-14T00:00:00Z','theme':'dark','completed':['01'],'review':['02'],'quiz':{},'drafts':{'01:base':'restored'},'lastLesson':'01'}
        (td/'valid.json').write_text(json.dumps(good,ensure_ascii=False),encoding='utf-8')
        # Prevent reload in about:blank test harness after successful validation; verify save before timer fires.
        page.locator('[data-import]').set_input_files(str(td/'valid.json'));page.wait_for_timeout(120)
        restored=stored_state(page)
        add('Valid import replaces data after validation',restored['completed']==['01'] and restored['review']==['02'] and restored['drafts'].get('01:base')=='restored')
        add('Valid import applies dark theme',page.locator('html').get_attribute('data-theme')=='dark')
    page.close()

    # Semantic / keyboard-oriented smoke checks on representative pages.
    for rel in ['index.html','lessons/01.html','lessons/16.html','lessons/32.html','settings.html','projects/index.html']:
        page,errs=new_page(ctx,rel,{'width':1440,'height':900})
        add(rel+' skip link',page.locator('a.skip-link').count()==1)
        add(rel+' main landmark',page.locator('main').count()==1)
        add(rel+' no positive tabindex',page.locator('[tabindex]').evaluate_all('(els)=>els.every(e=>Number(e.getAttribute("tabindex"))<=0)'))
        unnamed=page.locator('button').evaluate_all('(els)=>els.filter(e=>!(e.textContent.trim()||e.getAttribute("aria-label")||e.getAttribute("title"))).length')
        add(rel+' named buttons',unnamed==0,unnamed)
        page.keyboard.press('Tab');add(rel+' first Tab reaches skip link',page.evaluate('document.activeElement?.classList.contains("skip-link")===true'))
        page.close()
    browser.close()

failed=[x for x in results if not x[1]]
print(f'checks={len(results)} pass={len(results)-len(failed)} fail={len(failed)}')
for n,_,d in failed:print('FAIL',n,d)
(ROOT/'docs/browser_audit.json').write_text(json.dumps([{'name':n,'ok':ok,'detail':d} for n,ok,d in results],ensure_ascii=False,indent=2),encoding='utf-8')
sys.stdout.flush();sys.stderr.flush();os._exit(1 if failed else 0)
