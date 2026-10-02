import {createServer} from 'node:http';
import {readFile,writeFile} from 'node:fs/promises';
import {resolve,extname} from 'node:path';
import assert from 'node:assert/strict';
const {chromium}=await import(process.env.PLAYWRIGHT_MODULE);
const fixture=resolve(process.env.CSTUDY_FIXTURE),out=resolve('docs/validation/2026-10-02-import-storage/results.json');
const server=createServer(async(req,res)=>{try{const path=resolve(fixture,'.'+decodeURIComponent(new URL(req.url,'http://local').pathname));if(!path.startsWith(fixture+'/'))throw Error();const file=path.endsWith('/')?path+'index.html':path;res.setHeader('Content-Type',{'.html':'text/html','.js':'text/javascript','.css':'text/css','.json':'application/json'}[extname(file)]||'application/octet-stream');res.end(await readFile(file));}catch{res.writeHead(404);res.end();}});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const origin=`http://127.0.0.1:${server.address().port}`,key='cstudy.learning.v2',checks=[],errors=[];
let browser;
const record=(name,evidence,kind='actual HTTP UI')=>checks.push({name,status:'PASS',kind,evidence});
try{
 browser=await chromium.launch({headless:true});
 const context=await browser.newContext({acceptDownloads:true});const page=await context.newPage();page.setDefaultTimeout(7000);page.on('pageerror',e=>errors.push(e.message));
 const raw=()=>page.evaluate(k=>localStorage.getItem(k),key);
 const upload=async(name,contents)=>{await page.locator('[data-import]').setInputFiles({name,mimeType:'application/json',buffer:Buffer.from(contents)});await page.locator('[data-import-message]').filter({hasText:'読み込み失敗'}).waitFor();};
 await page.goto(origin+'/course/lessons/01.html');await page.locator('[data-draft="01:base"]').fill('Console.WriteLine("baseline preserved");');await page.waitForTimeout(350);await page.goto(origin+'/course/settings.html');
 const baseline=await raw();assert.equal(JSON.parse(baseline).drafts['01:base'],'Console.WriteLine("baseline preserved");');
 const valid={version:2,updatedAt:'2026-10-02T00:00:00Z',theme:'light',completed:['02'],review:['01'],quiz:{'01':{answers:[0,1,0,3,null],score:3}},drafts:{'01:base':'Console.WriteLine("valid import task6");'},lastLesson:'01'};
 for(const [name,contents,expected] of [
 ['invalid-version','{"version":99}','versionは2である必要があります'],
 ['malformed','not-json','JSONとして解析できません'],
 ['oversize','x'.repeat(524289),'512 KiBを超えています'],
 ['invalid-draft-key',JSON.stringify({...valid,drafts:{unknown:'bad'}}),'下書きのキーまたは長さが不正です'],
 ['invalid-quiz-answer',JSON.stringify({...valid,quiz:{'01':{answers:[4],score:0}}}),'quizの回答が不正です']
 ]){await upload(name+'.json',contents);const message=await page.locator('[data-import-message]').textContent();assert(message.includes(expected));assert.equal(await raw(),baseline);record(name,{message,storedBytesUnchanged:true});}
 const navigation=page.waitForEvent('load');await page.locator('[data-import]').setInputFiles({name:'valid.json',mimeType:'application/json',buffer:Buffer.from(JSON.stringify(valid))});await navigation;
 let imported=JSON.parse(await raw());const normalized=v=>{const {updatedAt,...rest}=v;return rest};assert.deepEqual(normalized(imported),normalized(valid));assert.equal(await page.locator('[data-theme-select]').inputValue(),'light');record('valid-import-reload',{state:imported,theme:'light'});
 const pending=page.waitForEvent('download');await page.locator('[data-export]').click();const download=await pending;assert.equal(download.suggestedFilename(),'cstudy-learning-data.json');const downloaded=await readFile(await download.path(),'utf8');assert.deepEqual(JSON.parse(downloaded),JSON.parse(await raw()));await writeFile(resolve('docs/validation/2026-10-02-import-storage/exported.json'),downloaded+'\n');record('export-download',{filename:download.suggestedFilename(),matchesStoredState:true,bytes:Buffer.byteLength(downloaded)});
 await page.goto(origin+'/course/lessons/01.html');assert.equal(await page.locator('[data-draft="01:base"]').inputValue(),valid.drafts['01:base']);assert.equal(await page.locator('[data-review="01"]').getAttribute('aria-pressed'),'true');const answers=await page.locator('input[type=radio]:checked').evaluateAll(nodes=>nodes.map(n=>Number(n.value)));assert.deepEqual(answers,[0,1,0,3]);record('import-restored-lesson',{draft:valid.drafts['01:base'],checkedAnswers:answers,review:true});
 // Fault injection is limited to Storage.setItem in a separate disposable browser context.
 const fault=await browser.newContext();await fault.addInitScript(()=>{Storage.prototype.setItem=function(){throw new DOMException('task-owned quota fault','QuotaExceededError')}});const fp=await fault.newPage();fp.setDefaultTimeout(7000);await fp.goto(origin+'/course/lessons/01.html');await fp.locator('[data-draft="01:base"]').fill('unsaved draft remains');await fp.locator('[data-draft-status]').filter({hasText:'未保存'}).first().waitFor();assert.equal(await fp.locator('[data-draft="01:base"]').inputValue(),'unsaved draft remains');assert.equal(await fp.evaluate(k=>localStorage.getItem(k),key),null);const warning=await fp.locator('[data-storage-warning]').textContent();assert(warning.includes('保存'));record('quota-draft-visible-failure',{warning,inputRetained:true,storedValue:null},'actual HTTP UI with injected Storage.setItem fault');
 await fp.goto(origin+'/course/settings.html');await fp.locator('[data-import]').setInputFiles({name:'valid.json',mimeType:'application/json',buffer:Buffer.from(JSON.stringify(valid))});await fp.locator('[data-import-message]').filter({hasText:'端末へ保存できません'}).waitFor();assert.equal(await fp.locator('[data-theme-select]').inputValue(),'system');assert.equal(await fp.evaluate(k=>localStorage.getItem(k),key),null);const rollbackDownload=fp.waitForEvent('download');await fp.locator('[data-export]').click();const rollback=JSON.parse(await readFile(await (await rollbackDownload).path(),'utf8'));assert.equal(rollback.theme,'system');assert.deepEqual(rollback.completed,[]);assert.deepEqual(rollback.drafts,{});record('quota-import-rollback',{inMemoryExport:rollback,message:await fp.locator('[data-import-message]').textContent(),themeRemains:'system',storedValue:null},'actual HTTP UI with injected Storage.setItem fault');
 assert.deepEqual(errors,[]);await fault.close();await context.close();
} catch(e){checks.push({name:'execution',status:'FAIL',error:String(e),stack:e.stack});process.exitCode=1;}
finally{const result={sourceBase:'f013ecf4f60498ce80e8d63909933de1535a9fb9',browser:browser?.version(),origin,checks,pageErrors:errors,scope:'Loopback HTTP /course/ subpath; fresh contexts. Native file-input setInputFiles and real Blob download. Quota faults explicitly injected. No published HTTPS/native Safari/physical device acceptance.'};await writeFile(out,JSON.stringify(result,null,2)+'\n');if(browser)await browser.close();await new Promise(r=>server.close(r));console.log(JSON.stringify(result,null,2));}
