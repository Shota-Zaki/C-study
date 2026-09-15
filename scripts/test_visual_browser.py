#!/usr/bin/env python3
"""Chromium in-memory UI tests.
This harness does NOT navigate a hosted URL. CSS/JS/images are loaded from files,
and localStorage is an explicitly substituted in-memory dictionary because the
rendering document has an opaque about:blank origin. Production code is unchanged.
"""
from pathlib import Path
from bs4 import BeautifulSoup as BS
from playwright.sync_api import sync_playwright
import base64,json,ast,sys,os,shutil
R=Path(__file__).resolve().parents[1];OUT=R/'validation/visual';OUT.mkdir(parents=True,exist_ok=True)
checks=[];failures=[];js_errors=[]

def markup(rel,store=None):
    p=R/rel;s=BS(p.read_text(),'html.parser')
    for link in list(s.select('link[rel="stylesheet"]')):
        f=(p.parent/link['href']).resolve();style=s.new_tag('style');style.string=f.read_text();link.replace_with(style)
    for img in s.select('img[src]'):
        f=(p.parent/img['src']).resolve()
        if f.is_file():img['src']='data:image/svg+xml;base64,'+base64.b64encode(f.read_bytes()).decode();img.attrs.pop('loading',None)
    for el in s.select('script[src]'):
        f=(p.parent/el['src']).resolve();el.attrs.pop('src');el.attrs.pop('defer',None);el.string=f.read_text()
    harness=s.new_tag('script');harness.string='window.__store='+json.dumps(store or {})+";Object.defineProperty(window,'localStorage',{configurable:true,value:{getItem(k){return window.__store[k]??null},setItem(k,v){window.__store[k]=String(v)},removeItem(k){delete window.__store[k]}}});";s.head.insert(0,harness)
    return str(s)

def record(name,ok,detail=''):
    checks.append({'name':name,'pass':bool(ok),'detail':detail})
    if not ok:failures.append(name+': '+str(detail))
    (OUT/'browser-progress.json').write_text(json.dumps(checks,ensure_ascii=False))
    print(('PASS ' if ok else 'FAIL ')+name,flush=True)

def new_page(browser,rel,width=1536,height=1040,dark=False,store=None):
    pg=browser.new_page(viewport={'width':width,'height':height},device_scale_factor=1,color_scheme='dark' if dark else 'light')
    pg.set_default_timeout(5000)
    pg.on('pageerror',lambda e:js_errors.append({'page':rel,'error':str(e)}))
    pg.set_content(markup(rel,store),wait_until='load');pg.evaluate('scrollTo(0,0)');pg.wait_for_timeout(80)
    return pg

with sync_playwright() as p:
    browser_path=os.environ.get('CSTUDY_CHROMIUM') or shutil.which('chromium') or shutil.which('chromium-browser')
    browser=p.chromium.launch(**({'executable_path':browser_path} if browser_path else {}),headless=True,args=['--no-sandbox'])
    # Rendering samples from all 8 chapters and all 5 non-lesson page types.
    for rel in ([] if os.environ.get('ONLY_FUNCTIONAL') else ['lessons/01.html','lessons/05.html','lessons/09.html','lessons/13.html','lessons/18.html','lessons/24.html','lessons/27.html','lessons/32.html','deep-dives/21.html','index.html','guides/glossary.html','guides/learning-workflow.html','projects/index.html','settings.html']):
        for width,height in [(1536,1040),(1024,900),(390,844)]:
            pg=new_page(browser,rel,width,height)
            sizes=pg.evaluate('({viewport:innerWidth,width:document.documentElement.scrollWidth,height:document.documentElement.scrollHeight})')
            record(f'layout/{rel}/{width}',sizes['width']<=width,sizes)
            num=pg.locator('body').get_attribute('data-current-lesson')
            if num:
                record(f'chapter/{rel}/{width}',pg.locator('.current-chapter[open]').count()==1)
                record(f'terms/{rel}/{width}',pg.locator('.glossary-panel').evaluate('(e)=>e.open')==(width>1180))
            if (rel,width) in [('lessons/05.html',1536),('lessons/13.html',390),('index.html',1536),('lessons/24.html',1024)]:pg.screenshot(path=str(OUT/f'{Path(rel).parent.name}-{Path(rel).stem}-{width}.png'))
            pg.close()
    # Desktop local TOC and rail use different scroll containers.
    pg=new_page(browser,'lessons/05.html')
    pg.locator('.lesson-toc a[href="#worked-case-heading"]').click();pg.wait_for_timeout(100)
    record('toc/anchor-scroll',pg.locator('#worked-case-heading').evaluate('(e)=>e.getBoundingClientRect().top')>=100)
    record('toc/current-section',pg.locator('.lesson-toc a[href="#worked-case-heading"]').get_attribute('aria-current')=='location')
    pg.screenshot(path=str(OUT/'desktop-example.png'))
    link=pg.locator('.article .term-link').first
    link.scroll_into_view_if_needed();y=pg.evaluate('scrollY');target=link.get_attribute('href');link.click();pg.wait_for_timeout(100)
    record('terms/reveal-definition',pg.locator(target).evaluate('(e)=>e.open'))
    record('terms/preserve-article-position',abs(pg.evaluate('scrollY')-y)<3)
    pg.close()
    # Mobile drawer from both menu controls and safe focus return.
    pg=new_page(browser,'lessons/13.html',390,844)
    pg.locator('[data-show-toc]').click();record('mobile/toc-opens-drawer',pg.locator('.left-nav').evaluate('(e)=>e.classList.contains("open")'))
    pg.keyboard.press('Escape');record('mobile/escape-closes-drawer',not pg.locator('.left-nav').evaluate('(e)=>e.classList.contains("open")'))
    pg.locator('[data-drawer="open"]').click();record('mobile/menu-opens-drawer',pg.locator('.left-nav').evaluate('(e)=>e.classList.contains("open")'))
    pg.screenshot(path=str(OUT/'mobile-navigation.png'));pg.locator('[data-drawer="close"]').click()
    pg.locator('.terms-toggle').click();record('mobile/terms-expand',pg.locator('.glossary-panel').evaluate('(e)=>e.open'))
    pg.close()
    # Draft editing/export, previous-version persistence format, and quiz state.
    pg=new_page(browser,'lessons/05.html')
    draft=pg.locator('textarea[data-draft]').first
    record('draft/starter-present',len(draft.input_value())>0)
    value='Console.WriteLine("draft test");';draft.fill(value);pg.wait_for_timeout(400)
    store=pg.evaluate('window.__store');key=next((k for k in store if 'cstudy.learning' in k),'')
    state=json.loads(store[key]);draft_key=draft.get_attribute('data-draft')
    record('draft/save-in-storage-harness',state['drafts'][draft_key]==value)
    pg.evaluate('''document.querySelectorAll('.question').forEach(q=>{const r=q.querySelector('input[value="'+q.dataset.answer+'"]');r.checked=true;r.dispatchEvent(new Event('change',{bubbles:true}))})''')
    pg.locator('[data-grade]').click();record('quiz/all-correct', '5 / 5' in pg.locator('[data-quiz-result]').inner_text())
    pg.locator('[data-complete]').click();record('progress/completed',pg.locator('[data-complete]').get_attribute('aria-pressed')=='true')
    pg.locator('[data-review]').click();record('progress/review',pg.locator('[data-review]').get_attribute('aria-pressed')=='true')
    with pg.expect_download() as capture:pg.locator('[data-download-draft]').first.click()
    download=capture.value;record('draft/cs-download',Path(download.path()).read_text()==value)
    pg.locator('[data-open-search]').click();pg.locator('#search-dialog input').fill('送料');record('search/keyword',pg.locator('.search-result').count()>0)
    pg.keyboard.press('Escape')
    wrap=pg.locator('[data-wrap-code]').first;wrap.click();record('code/wrap-toggle',wrap.get_attribute('aria-pressed')=='true')
    store=pg.evaluate('window.__store');pg.close()
    pg=new_page(browser,'lessons/05.html',store=store)
    record('draft/restore-in-storage-harness',pg.locator('textarea[data-draft]').first.input_value()==value)
    record('progress/restore-in-storage-harness',pg.locator('[data-complete]').get_attribute('aria-pressed')=='true')
    pg.close()
    pg=new_page(browser,'guides/glossary.html');pg.locator('#term-filter').fill('nullable');record('glossary/filter',pg.locator('.term-entry:visible').count()>0 and pg.locator('.term-entry:visible').count()<180);pg.close()
    pg=new_page(browser,'lessons/05.html',dark=True);record('theme/system-dark',pg.locator('html').get_attribute('data-theme')=='dark');pg.screenshot(path=str(OUT/'desktop-dark.png'));pg.close()
    # Inspect every authored SVG's text boundaries using the browser's actual font metrics.
    for path in sorted((R/'assets/diagrams').glob('*.svg')):
        pg=browser.new_page(viewport={'width':800,'height':450});pg.set_content(path.read_text())
        boxes=pg.evaluate('''()=>{const svg=document.querySelector('svg'),v=svg.viewBox.baseVal;return [...svg.querySelectorAll('text')].filter(t=>{const b=t.getBBox();return b.x<0||b.y<0||b.x+b.width>v.width||b.y+b.height>v.height}).map(t=>t.textContent)}''')
        record('svg/bounds/'+path.name,not boxes,boxes);pg.close()
    browser.close()
# Lexical checks only: do not mislabel as a compiler result.
t=ast.parse((R/'scripts/audit_csharp_code.py').read_text());fn=next(x for x in t.body if isinstance(x,ast.FunctionDef) and x.name=='scan');ns={};exec(compile(ast.Module(body=[fn],type_ignores=[]),'scanner','exec'),ns)
visual=json.loads((R/'content/visual/lessons.json').read_text())
for num,item in visual.items():
    for kind in ('case','detail'):
        issues=ns['scan'](item[kind]['code']);record(f'csharp/lexical-only/{num}/{kind}',not issues,issues)
record('javascript/no-uncaught-errors',not js_errors,js_errors)
report={'status':'PASS' if not failures else 'FAIL','checks':len(checks),'passed':sum(x['pass'] for x in checks),'failed':failures,'environment':'Chromium / in-memory HTML with inline local assets; test-only localStorage substitute','unverified':['Real HTTP/HTTPS navigation (browser administrator restriction)','Real origin localStorage persistence','C# compilation/execution','Safari/iPhone/iPad physical devices','Deployment to GitHub Pages/Cloudflare'],'results':checks,'javascript_errors':js_errors}
(OUT/'browser-audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items() if k not in ('results',)},ensure_ascii=False,indent=2));sys.exit(bool(failures))
