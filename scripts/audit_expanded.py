#!/usr/bin/env python3
"""Static and actual Chromium/HTTP checks. Never compiles or executes C#."""
from __future__ import annotations
from pathlib import Path
import json,re,threading,http.server,functools,urllib.parse,hashlib,time,os
from collections import Counter
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'docs/validation';OUT.mkdir(parents=True,exist_ok=True)
PAGES=json.loads((ROOT/'content/published-pages.json').read_text())

def static_audit():
 docs={rel:BeautifulSoup((ROOT/rel).read_text(),'html.parser') for rel in PAGES};issues=[];links=0;stats=[]
 for rel,s in docs.items():
  ids=[e['id'] for e in s.select('[id]')]
  if len(ids)!=len(set(ids)):issues.append([rel,'duplicate_ids'])
  if len(s.select('h1'))!=1:issues.append([rel,'h1_count',len(s.select('h1'))])
  for a in s.select('[href],[src]'):
   url=a.get('href') or a.get('src');u=urllib.parse.urlsplit(url)
   if u.scheme or u.netloc or url.startswith(('mailto:','tel:','data:')):continue
   links+=1;path=urllib.parse.unquote(u.path)
   dest=(ROOT/rel).parent/path if path else ROOT/rel
   dest=dest.resolve()
   try:key=str(dest.relative_to(ROOT))
   except ValueError:issues.append([rel,'outside_root',url]);continue
   if dest.is_dir():dest=dest/'index.html';key=str(dest.relative_to(ROOT))
   if not dest.exists():issues.append([rel,'missing_target',url]);continue
   if u.fragment and dest.suffix=='.html':
    ds=docs.get(key)
    if ds is None:ds=BeautifulSoup(dest.read_text(),'html.parser')
    if not ds.find(id=urllib.parse.unquote(u.fragment)):issues.append([rel,'missing_fragment',url])
  for control in s.select('textarea,input:not([type="hidden"]),select'):
   has_label=control.get('aria-label') or control.get('aria-labelledby') or control.find_parent('label') or (control.get('id') and s.find('label',attrs={'for':control['id']}))
   if not has_label:issues.append([rel,'unlabelled_input',str(control)[:100]])
  art=s.select_one('.article');text=art.get_text(' ',strip=True)
  stats.append({'page':rel,'textCharacters':len(text),'h2':len(art.select('h2')),'codeBlocks':len(art.select('pre code')),'tables':len(art.select('table')),'diagrams':len(art.select('.concept-diagram')),'questions':len(art.select('.question')),'optionDetails':len(art.select('.reason-detail')),'exerciseCoaching':len(art.select('.exercise-input')),'localTerms':len(art.select('.local-terms .term-entry'))})
  if rel.startswith('lessons/'):
   if len(art.select('.reason-detail'))!=20:issues.append([rel,'option_explanation_count'])
   if len(art.select('.exercise-input'))!=3:issues.append([rel,'exercise_coaching_count'])
   if len(art.select('.expanded-preview .detail-section'))!=2:issues.append([rel,'concept_preview_missing'])
  if re.search(r'Java Silver|Java経験|Javaとの比較|Python経験|JavaScript経験|長くなるので割愛|詳細は公式ドキュメント参照',text,re.I):issues.append([rel,'disallowed_teaching_phrase'])
 result={'type':'static_html','pages':len(PAGES),'localReferencesChecked':links,'issues':issues,'status':'PASS' if not issues else 'FAIL','pagesMetrics':stats}
 (OUT/'static.json').write_text(json.dumps(result,ensure_ascii=False,indent=2));return result

class Quiet(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*args):pass

def http_smoke():
 import urllib.request
 server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(ROOT)))
 threading.Thread(target=server.serve_forever,daemon=True).start();results=[]
 try:
  for rel in PAGES:
   try:
    with urllib.request.urlopen(f'http://127.0.0.1:{server.server_address[1]}/{rel}',timeout=4) as response:
     data=response.read();results.append({'page':rel,'status':response.status,'bytes':len(data),'ok':response.status==200 and b'<html' in data})
   except Exception as exc:results.append({'page':rel,'ok':False,'error':str(exc)})
 finally:server.shutdown();server.server_close()
 result={'mode':'Python urllib through actual loopback HTTP, not browser navigation','status':'PASS' if all(x['ok'] for x in results) else 'FAIL','results':results};(OUT/'http.json').write_text(json.dumps(result,ensure_ascii=False,indent=2));return result

def browser_audit():
 """Render exact generated HTML/CSS/JS directly. Native URL navigation is blocked.
 Local storage is replaced only in the test page by a transparent in-memory adapter.
 These are DOM/logic tests, not end-to-end browser persistence tests.
 """
 results=[];interactions=[];screens=[];events=[]
 prior=OUT/('browser-'+os.environ.get('AUDIT_MODE','all')+'-pages.json')
 if os.environ.get('AUDIT_RESUME') and prior.exists():results=json.loads(prior.read_text())
 def check(name,ok,detail='DOM rendering / memory-storage adapter'):
  interactions.append({'name':name,'status':'PASS' if ok else 'FAIL','detail':detail})
 cache={}
 for rel in PAGES:
  doc=BeautifulSoup((ROOT/rel).read_text(),'html.parser');scripts=[];styles=[]
  for link in doc.select('link[rel="stylesheet"]'):
   styles.append(((ROOT/rel).parent/link['href']).resolve().read_text());link.decompose()
  for script in doc.select('script[src]'):
   scripts.append(((ROOT/rel).parent/script['src']).resolve().read_text());script.decompose()
  for link in doc.select('link[rel="icon"],link[rel="canonical"]'):link.decompose()
  cache[rel]=(str(doc),'\n'.join(styles),scripts)
 with sync_playwright() as pw:
  browser=pw.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox'])
  def load(context,rel,store=None,denied=False):
   page=context.new_page();errs=[];page.on('pageerror',lambda e:errs.append(str(e)))
   markup,css,scripts=cache[rel];page.set_content(markup,wait_until='load');page.add_style_tag(content=css)
   page.evaluate('''({initial,denied}) => { const map=new Map(Object.entries(initial));const adapter={getItem(k){return map.has(k)?map.get(k):null},setItem(k,v){if(denied)throw new DOMException('Test denial','QuotaExceededError');map.set(String(k),String(v))},removeItem(k){map.delete(k)},clear(){map.clear()},key(i){return [...map.keys()][i]||null},get length(){return map.size}};Object.defineProperty(window,'localStorage',{value:adapter,configurable:true});window.__testStorageDump=()=>Object.fromEntries(map); }''',{'initial':store or {},'denied':denied})
   for script in scripts:page.add_script_tag(content=script)
   page.wait_for_timeout(10);return page,errs
  for mode,width,height in [('desktop',1440,1000),('tablet',834,1112),('mobile',390,844)]:
   if os.environ.get('AUDIT_MODE') and mode!=os.environ['AUDIT_MODE']:continue
   context=browser.new_context(viewport={'width':width,'height':height},device_scale_factor=1,reduced_motion='reduce')
   scanned=0
   for rel in PAGES:
    if any(r['page']==rel and r['viewport']==mode for r in results):continue
    if scanned>=int(os.environ.get('AUDIT_PAGE_LIMIT','1000')):break
    scanned+=1
    page,errors=load(context,rel)
    metrics=page.evaluate('''() => {const w=innerWidth;const over=[...document.querySelectorAll('.article section,.article h1,.article h2,.article h3,.article p,.article li,.article .codebox,.article .table-scroll,.article figure,.article textarea,.article .exercise')].filter(e=>{const clip=e.closest('.codebox,.table-scroll');if(clip&&clip!==e)return false;const r=e.getBoundingClientRect();return r.width&&((r.right>w+2)||(r.left< -2));}).slice(0,12).map(e=>({tag:e.tagName,cls:e.className,x:e.getBoundingClientRect().x,width:e.getBoundingClientRect().width}));return {bodyWidth:document.documentElement.scrollWidth,viewport:w,overflow:over,position:!!document.querySelector('.reading-position'),h1:document.querySelectorAll('h1').length};}''')
    page.evaluate('window.scrollTo({top:document.body.scrollHeight/2,behavior:"instant"})');page.wait_for_timeout(10)
    if not page.locator('.reading-title').text_content():errors.append('reading position empty')
    page.evaluate('window.scrollTo({top:document.body.scrollHeight,behavior:"instant"})');page.wait_for_timeout(5)
    issues=list(errors)
    if metrics['bodyWidth']>width+2:issues.append('page_horizontal_overflow')
    if metrics['overflow']:issues.append('visible_content_overflow')
    print(mode,rel,'issues',issues,flush=True)
    results.append({'page':rel,'viewport':mode,'width':width,'height':height,'metrics':metrics,'issues':issues,'status':'PASS' if not issues else 'FAIL'})
    page.close()
    (OUT/('browser-'+mode+'-pages.json')).write_text(json.dumps(results,ensure_ascii=False,indent=2))
   for rel,anchor in [('deep-dives/13.html','#detail-h2-03'),('lessons/19.html','#quiz'),('guides/async-timeline.html','#guide-h2-02')]:
    page,_=load(context,rel);page.locator(anchor).evaluate('e=>e.scrollIntoView({block:"start",behavior:"instant"})');page.wait_for_timeout(60)
    name=f'{mode}-{Path(rel).stem}-{anchor[1:]}.png';page.screenshot(path=str(OUT/name),full_page=False);screens.append(name);page.close()
   context.close()
  context=browser.new_context(viewport={'width':1440,'height':1000},reduced_motion='reduce')
  page,errors=load(context,'lessons/01.html');page.locator('textarea[data-draft="01:base"]').fill('Console.WriteLine("下書き保存の確認");');page.wait_for_timeout(350)
  store=page.evaluate('__testStorageDump()');page.close();page,errors=load(context,'lessons/01.html',store)
  check('draft serialization and restoration',page.locator('textarea[data-draft="01:base"]').input_value()=='Console.WriteLine("下書き保存の確認");')
  page.locator('[data-complete]').first.click();store=page.evaluate('__testStorageDump()');page.close();page,_=load(context,'lessons/01.html',store);check('v2 progress restoration',page.locator('[data-complete]').first.get_attribute('aria-pressed')=='true')
  for q in page.locator('.question').all():q.locator('input[value="0"]').check()
  page.locator('[data-grade]').click();check('all 20 option explanations visible',page.locator('.choice-explain:visible').count()==20)
  check('quiz and draft distinguished','確認問題' in page.locator('[data-quiz-result]').text_content())
  page.locator('[data-open-search]').first.click();page.locator('#search-dialog input').fill('協調');check('search includes detailed content',page.locator('.search-result[href*="deep-dives"]').count()>0);page.keyboard.press('Escape');page.close()
  page,_=load(context,'deep-dives/13.html');link=page.locator('a.term-link').first;target=link.get_attribute('href');link.click();page.wait_for_timeout(70);check('local definition opens through hash link',page.locator(target).get_attribute('open') is not None)
  button=page.locator('[data-wrap-code]').first;button.click();check('code wrapping',button.get_attribute('aria-pressed')=='true')
  heading=page.locator('#detail-h2-03');heading.evaluate('e=>e.scrollIntoView({block:"start",behavior:"instant"})');page.wait_for_timeout(60);check('anchor position matches current heading',page.locator('.reading-title').text_content()==heading.text_content())
  page.locator('[data-copy]').first.click();page.wait_for_timeout(100);check('copy denial does not crash page',page.locator('h1').count()==1,'Clipboard is blocked by policy; success is not claimed.');page.close()
  page,_=load(context,'guides/glossary.html');page.locator('#term-filter').fill('IL');check('glossary filtering',0<page.locator('.term-entry:visible').count()<180);page.close()
  page,_=load(context,'settings.html',store);page.locator('[data-theme-select]').select_option('dark');check('dark theme',page.locator('html').get_attribute('data-theme')=='dark');store=page.evaluate('__testStorageDump()');page.close();page,_=load(context,'settings.html',store);check('theme restoration',page.locator('html').get_attribute('data-theme')=='dark')
  before=page.evaluate('localStorage.getItem("cstudy.learning.v2")');page.locator('[data-import]').set_input_files({'name':'invalid.json','mimeType':'application/json','buffer':b'{"version":99}'});page.wait_for_timeout(40);check('invalid import preserves previous values',before==page.evaluate('localStorage.getItem("cstudy.learning.v2")'))
  export=json.loads(before);export['review']=['02'];page.locator('[data-import]').set_input_files({'name':'valid.json','mimeType':'application/json','buffer':json.dumps(export).encode()});page.wait_for_timeout(70);check('valid import validates and stores values',json.loads(page.evaluate('localStorage.getItem("cstudy.learning.v2")'))['review']==['02']);page.close()
  corrupt={'cstudy.learning.v2':'{invalid saved data'};page,_=load(context,'lessons/01.html',corrupt);check('corrupt prior storage is not overwritten',page.evaluate('localStorage.getItem("cstudy.learning.v2")')=='{invalid saved data');page.close()
  page,_=load(context,'lessons/01.html',denied=True);page.locator('textarea').first.fill('保存失敗でも保持する下書き');page.wait_for_timeout(350);check('save failure is visible and input remains',page.locator('[data-storage-warning]').is_visible() and '未保存' in page.locator('[data-draft-status]').first.text_content() and page.locator('textarea').first.input_value()=='保存失敗でも保持する下書き');page.close()
  mobile=browser.new_context(viewport={'width':390,'height':844});page,_=load(mobile,'lessons/01.html');page.locator('[data-drawer="open"]').click();check('mobile navigation opens',page.locator('.left-nav').evaluate('e=>e.classList.contains("open")'));page.keyboard.press('Escape');check('mobile Escape restores focus',page.locator('[data-drawer="open"]').evaluate('e=>e===document.activeElement'));page.close();mobile.close()
  narrow=browser.new_context(viewport={'width':320,'height':780});page,_=load(narrow,'deep-dives/32.html');check('320px width reflow',page.evaluate('document.documentElement.scrollWidth<=innerWidth+2'));page.close();narrow.close()
  page,_=load(context,'deep-dives/32.html');page.evaluate('document.documentElement.style.zoom="2"');check('CSS 200 percent zoom reflow',page.evaluate('document.documentElement.scrollWidth<=innerWidth+2'),'CSS zoom simulation, not native browser UI zoom');page.close()
  # Screen evidence of ordinary desktop/mobile entry points and dark mode.
  for rel,name in [('index.html','desktop-home.png'),('deep-dives/01.html','desktop-detail-top.png'),('guides/glossary.html','desktop-glossary.png')]:
   page,_=load(context,rel,store);page.screenshot(path=str(OUT/name));screens.append(name);page.close()
  context.close();browser.close()
 result={'artifactFingerprint':hashlib.sha256(''.join(hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in PAGES+['assets/css/expanded.css','assets/js/site.js','assets/js/expanded.js']).encode()).hexdigest(),'browser':'Chromium /usr/bin/chromium','mode':'Direct DOM injection of generated HTML/CSS/JS. Memory-only localStorage adapter for logic testing.','nativeNavigation':'UNVERIFIED: all URLs blocked by browser administrative policy; HTTP and file:// attempts failed','nativePersistence':'UNVERIFIED: real origin reload/storage and downloaded export file were not tested','physicalDevices':'UNVERIFIED: no physical tablet/mobile/Safari','pageChecks':len(results),'results':results,'interactions':interactions,'screenshots':screens,'status':'PASS' if all(x['status']=='PASS' for x in results+interactions) else 'FAIL'}
 (OUT/('browser-'+os.environ.get('AUDIT_MODE','all')+'.json')).write_text(json.dumps(result,ensure_ascii=False,indent=2));return result

if __name__=='__main__':
 start=time.time();s=static_audit();print('STATIC',s['status'],'issues',len(s['issues']),flush=True)
 h=http_smoke();print('HTTP',h['status'],'pages',len(h['results']),flush=True)
 b=browser_audit();print('BROWSER DOM',b['status'],'page checks',b['pageChecks'],'page failures',sum(x['status']=='FAIL' for x in b['results']),'interaction failures',[x['name'] for x in b['interactions'] if x['status']=='FAIL'],'seconds',round(time.time()-start,2),flush=True)

if __name__=="__main__":
 raise SystemExit(0 if s["status"]==h["status"]==b["status"]=="PASS" else 1)
