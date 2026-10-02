import {createServer} from 'node:http';
import {readFile,writeFile} from 'node:fs/promises';
import {resolve,extname} from 'node:path';
import assert from 'node:assert/strict';
const {chromium}=await import(process.env.PLAYWRIGHT_MODULE);
const fixture=resolve(process.env.CSTUDY_FIXTURE),out=resolve('docs/validation/2026-10-02-responsive-keyboard-read/results.json');
const server=createServer(async(req,res)=>{try{const path=resolve(fixture,'.'+decodeURIComponent(new URL(req.url,'http://local').pathname));if(!path.startsWith(fixture+'/'))throw Error();const file=path.endsWith('/')?path+'index.html':path;res.setHeader('Content-Type',{'.html':'text/html','.js':'text/javascript','.css':'text/css','.json':'application/json'}[extname(file)]||'application/octet-stream');res.end(await readFile(file));}catch{res.writeHead(404);res.end();}});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const origin=`http://127.0.0.1:${server.address().port}`,key='cstudy.learning.v2',checks=[],errors=[];
let browser;
const record=(name,evidence,kind='actual HTTP UI')=>checks.push({name,status:'PASS',kind,evidence});
try{
 browser=await chromium.launch({headless:true});
 const context=await browser.newContext();const page=await context.newPage();page.setDefaultTimeout(5000);page.on('pageerror',e=>errors.push(e.message));
 const pages=['lessons/01.html','lessons/05.html','lessons/09.html','lessons/13.html','lessons/18.html','lessons/24.html','lessons/27.html','lessons/32.html','deep-dives/21.html','index.html','guides/glossary.html','guides/learning-workflow.html','projects/index.html','settings.html'];
 for(const path of pages)for(const [width,height] of [[1536,1040],[1024,900],[390,844]]){
  await page.setViewportSize({width,height});await page.goto(origin+'/course/'+path);const sizes=await page.evaluate(()=>({viewport:innerWidth,width:document.documentElement.scrollWidth,height:document.documentElement.scrollHeight,h1:document.querySelector('h1')?.textContent}));
  checks.push({name:`layout/${path}/${width}`,status:sizes.width<=width?'PASS':'FAIL',kind:'actual HTTP UI geometry',evidence:sizes});
  if(['lessons/05.html/1536','lessons/13.html/390','index.html/1536','lessons/24.html/1024'].includes(path+'/'+width))await page.screenshot({path:resolve('docs/validation/2026-10-02-responsive-keyboard-read/'+path.replaceAll('/','-')+'-'+width+'.png')});
 }
 const test=async(name,run,kind='actual HTTP UI keyboard')=>{try{record(name,await run(),kind)}catch(e){checks.push({name,status:'FAIL',kind,error:String(e)});}};
 await page.setViewportSize({width:390,height:844});await page.goto(origin+'/course/lessons/13.html');
 await test('drawer-keyboard-open-trap-close',async()=>{
  await page.locator('[data-drawer="open"]').focus();await page.keyboard.press('Enter');assert.equal(await page.locator('[data-drawer="open"]').getAttribute('aria-expanded'),'true');
  const count=await page.locator('.left-nav').evaluate(nav=>[...nav.querySelectorAll('a,button,input,select,summary,[tabindex="0"]')].filter(n=>n.getClientRects().length).length);
  for(let i=0;i<count+2;i++){await page.keyboard.press('Tab');assert(await page.locator('.left-nav').evaluate(nav=>nav.contains(document.activeElement)));}
  await page.keyboard.press('Escape');assert.equal(await page.locator('[data-drawer="open"]').getAttribute('aria-expanded'),'false');assert(await page.locator('[data-drawer="open"]').evaluate(n=>n===document.activeElement));return {tabTransitions:count+2,focusRestored:true};
 });
 await test('search-shortcut-Escape-focus',async()=>{await page.keyboard.press('Control+k');assert(await page.locator('#search-dialog').evaluate(d=>d.open));assert(await page.locator('#search-dialog input').evaluate(n=>n===document.activeElement));await page.keyboard.press('Escape');assert.equal(await page.locator('#search-dialog').evaluate(d=>d.open),false);return {openedAndFocused:true,closed:true};});
 await test('slash-kept-in-textarea',async()=>{const area=page.locator('[data-draft]').first();await area.fill('');await area.focus();await page.keyboard.press('/');assert.equal(await area.inputValue(),'/');assert.equal(await page.locator('#search-dialog').evaluate(d=>d.open),false);return {draft:'/',searchClosed:true};});
 await test('radio-arrow-and-space-complete',async()=>{const radios=page.locator('.question').first().locator('input[type=radio]');await radios.first().focus();await page.keyboard.press('Space');assert(await radios.first().isChecked());await page.keyboard.press('ArrowDown');assert(await radios.nth(1).isChecked());const complete=page.locator('[data-complete="13"]');await complete.focus();await page.keyboard.press('Space');assert.equal(await complete.getAttribute('aria-pressed'),'true');return {radioArrowSelectsNext:true,completionSpaceToggles:true};});
 await context.close();
 const valid={version:2,updatedAt:'2026-10-02T00:00:00Z',theme:'dark',completed:['02'],review:[],quiz:{},drafts:{'01:base':'recovered draft'},lastLesson:null};
 for(const mode of ['corrupt-json','read-denied']){
  const fault=await browser.newContext();const fp=await fault.newPage();fp.setDefaultTimeout(5000);const pageErrors=[];fp.on('pageerror',e=>pageErrors.push(e.message));
  if(mode==='corrupt-json'){await fp.goto(origin+'/course/settings.html');await fp.evaluate(k=>localStorage.setItem(k,'task-owned malformed preserved'),key);await fp.reload();}
  else {await fault.addInitScript(()=>{const original=Storage.prototype.getItem;window.__readStored=k=>original.call(localStorage,k);Storage.prototype.getItem=function(){throw new DOMException('task-owned read denial','SecurityError')}});await fp.goto(origin+'/course/settings.html');}
  const stored=()=>fp.evaluate(({key,mode})=>mode==='read-denied'?window.__readStored(key):localStorage.getItem(key),{key,mode});const before=await stored();
  await test(mode+'-protect-and-warn',async()=>{const message=await fp.locator('[data-storage-warning]').textContent();assert(message.includes('読み込め'));await fp.goto(origin+'/course/lessons/01.html');await fp.locator('[data-draft="01:base"]').fill('visible blocked draft');await fp.locator('[data-draft-status]').filter({hasText:'未保存'}).first().waitFor();assert.equal(await stored(),before);assert.equal(await fp.locator('[data-draft="01:base"]').inputValue(),'visible blocked draft');return {warning:message,storedBytesBefore:before,storedBytesUnchanged:true,inputRetained:true};},'actual HTTP UI with injected '+mode+' fixture');
  await test(mode==='corrupt-json'?'corrupt-json-valid-backup-recovery':'read-denied-backup-write-fault-persists',async()=>{await fp.goto(origin+'/course/settings.html');const reload=fp.waitForEvent('load');await fp.locator('[data-import]').setInputFiles({name:'recovery.json',mimeType:'application/json',buffer:Buffer.from(JSON.stringify(valid))});await reload;const recovered=JSON.parse(await stored());assert.equal(recovered.theme,'dark');assert.deepEqual(recovered.completed,['02']);assert.equal(recovered.drafts['01:base'],'recovered draft');assert.deepEqual(pageErrors,[]);if(mode==='corrupt-json'){assert(await fp.locator('[data-storage-warning]').isHidden());await fp.goto(origin+'/course/lessons/01.html');assert.equal(await fp.locator('[data-draft="01:base"]').inputValue(),'recovered draft');assert.equal(await fp.locator('[data-storage-warning]').isHidden(),true);}else{assert(await fp.locator('[data-storage-warning]').isVisible());assert((await fp.locator('[data-storage-warning]').textContent()).includes('読み込め'));}return {storedState:recovered,warningAfterReload:await fp.locator('[data-storage-warning]').textContent(),readFaultPersists:mode==='read-denied'};},'actual HTTP UI with injected '+mode+' fixture');
  await fault.close();
 }
 assert.deepEqual(errors,[]);
}catch(e){checks.push({name:'execution',status:'FAIL',error:String(e),stack:e.stack});}
finally{const result={sourceBase:'7d0048fe6b629f8bb224f7bd3dd405190fa83959',browser:browser?.version(),origin,checks,pageErrors:errors,scope:'Loopback HTTP /course/; 14 representative pages x3 established widths; selected keyboard paths; injected corrupt-storage/read-denial cases. Not native Safari, devices, native zoom or published HTTPS.'};await writeFile(out,JSON.stringify(result,null,2)+'\n');if(browser)await browser.close();await new Promise(r=>server.close(r));console.log(JSON.stringify({browser:result.browser,checks:checks.length,failures:checks.filter(c=>c.status==='FAIL')},null,2));if(checks.some(c=>c.status==='FAIL'))process.exitCode=1;}
