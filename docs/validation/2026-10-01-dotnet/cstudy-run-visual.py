import json,subprocess,time,concurrent.futures
from pathlib import Path
repo=Path('/Volumes/ZAKKO_DEV/repos/C-study')
entries=json.loads((repo/'content/visual/sample-manifest.json').read_text())
container='cstudy-sdk-20261001'
def command(args,timeout=20):
 r=subprocess.run(['docker','exec',container,*args],capture_output=True,text=True,timeout=timeout)
 return {'exitCode':r.returncode,'output':r.stdout,'stderr':r.stderr}
def run(entry):
 dll=entry['path']+'/bin/Debug/net10.0/Example.dll'
 r=command(['timeout','15','dotnet',dll])
 expected=(repo/entry['path']/'expected.txt').read_text()
 return {'project':entry['path'],'expected':expected,**r,'passed':r['exitCode']==0 and r['output'].replace('\r\n','\n')==expected.replace('\r\n','\n')}
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
 results=list(pool.map(run,[e for e in entries if e['kind']=='csharp']))
http=[]
for lesson,cases in [('29',[('GET','/health',None,200,{'status':'ok'}),('GET','/products/1',None,200,{'id':1,'name':'Notebook'}),('GET','/products/9',None,404,None)]),('30',[('POST','/tasks/validate',{'title':'  Review  '},200,{'title':'Review'}),('POST','/tasks/validate',{'title':'   '},400,None)])]:
 dll=f'samples/visual/{lesson}/case/bin/Debug/net10.0/Example.dll'
 with open('/tmp/cstudy-http-'+lesson+'.log','w') as log:
  process=subprocess.Popen(['docker','exec',container,'timeout','25','dotnet',dll,'--urls','http://127.0.0.1:5189'],stdout=log,stderr=log)
  try:
   for attempt in range(50):
    ready=command(['curl','-s','-o','/dev/null','--max-time','1','http://127.0.0.1:5189/'])
    if ready['exitCode']==0:break
    if process.poll() is not None:raise RuntimeError('Web server exited')
    time.sleep(.1)
   else:raise RuntimeError('Web server did not become ready')
   for method,path,body,status,expected in cases:
    args=['curl','-sS','--max-time','3','-w','\n%{http_code}','-X',method]
    if body is not None:args+=['-H','Content-Type: application/json','--data',json.dumps(body)]
    r=command([*args,'http://127.0.0.1:5189'+path]);text,actual=r['output'].rsplit('\n',1)
    actual_body=json.loads(text) if text else None
    passed=r['exitCode']==0 and int(actual)==status and (expected is None or actual_body==expected)
    if lesson=='30' and status==400:passed=passed and 'title' in actual_body.get('errors',{})
    http.append({'lesson':lesson,'method':method,'path':path,'request':body,'expectedStatus':status,'actualStatus':int(actual),'body':actual_body,'passed':passed})
  finally:
   command(['pkill','-f','^dotnet '+dll])
   process.wait(timeout=5)
report={'console':results,'http':http,'allPassed':all(r['passed'] for r in results+http)}
Path('/tmp/cstudy-output-results.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
print('Console',len(results),'passed',sum(r['passed'] for r in results),'HTTP',len(http),'passed',sum(r['passed'] for r in http))
for r in results+http:
 if not r['passed']:print(r)
