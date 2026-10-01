import json,subprocess,time,datetime
from pathlib import Path
container='cstudy-sdk-20261001'
def command(args):
 r=subprocess.run(['docker','exec',container,*args],capture_output=True,text=True,timeout=10)
 return r
cases={
 '29/01':[('GET','/hello',None,200,{'message':'Hello, C#'})],
 '29/02':[('GET','/items/7',None,200,{'id':7,'name':'Item-7'}),('GET','/items/abc',None,404,None)],
 '29/03':[('GET','/greet',None,200,{'message':'Hello, Guest'}),('GET','/greet?name=%20Aoi%20',None,200,{'message':'Hello, Aoi'})],
 '30/01':[('POST','/validate-title',{'title':'  Review  '},200,{'title':'Review'}),('POST','/validate-title',{'title':' '},400,None),('POST','/validate-title',{'title':'A'*100},200,{'title':'A'*100}),('POST','/validate-title',{'title':'A'*101},400,None)],
 '30/02':[('POST','/todos',{'title':' '},400,None),('POST','/todos',{'title':' Review '},201,{'id':1,'title':'Review','done':False}),('GET','/todos/1',None,200,{'id':1,'title':'Review','done':False}),('DELETE','/todos/1',None,204,None),('GET','/todos/1',None,404,None),('DELETE','/todos/1',None,404,None)],
 '31/02':[('GET','/greeting',None,200,{'message':'UTC年:'+str(datetime.datetime.now(datetime.timezone.utc).year)})],
 '31/05':[('GET','/settings-summary',None,200,{'title':'C# Learning Lab','maxItems':100})],
 '32/01':[('GET','/todos',None,200,[]),('POST','/todos',{'title':' '},400,None),('POST','/todos',{'title':'Review'},201,{'id':1,'title':'Review','done':False}),('PUT','/todos/1/completion',{},400,None),('PUT','/todos/1/completion',{'done':True},200,{'id':1,'title':'Review','done':True}),('GET','/todos/1',None,200,{'id':1,'title':'Review','done':True}),('PUT','/todos/9/completion',{'done':True},404,None),('DELETE','/todos/1',None,204,None),('GET','/todos',None,200,[])]}
results=[]
for key,requests in cases.items():
 lesson,number=key.split('/')
 dll=f'samples/expanded/deep/{lesson}/example-{number}/bin/Debug/net10.0/Example.dll'
 with open('/tmp/cstudy-http-deep-'+lesson+'-'+number+'.log','w') as log:
  process=subprocess.Popen(['docker','exec',container,'timeout','25','dotnet',dll,'--urls','http://127.0.0.1:5189'],stdout=log,stderr=log)
  try:
   for attempt in range(50):
    ready=command(['curl','-s','-o','/dev/null','--max-time','1','http://127.0.0.1:5189/'])
    if ready.returncode==0:break
    if process.poll() is not None:raise RuntimeError('Web server exited')
    time.sleep(.1)
   else:raise RuntimeError('Web server not ready')
   for method,path,body,status,expected in requests:
    args=['curl','-sS','--max-time','3','-w','\n%{http_code}','-X',method]
    if body is not None:args+=['-H','Content-Type: application/json','--data',json.dumps(body)]
    r=command([*args,'http://127.0.0.1:5189'+path]);text,actual=r.stdout.rsplit('\n',1);actual_body=json.loads(text) if text else None
    passed=r.returncode==0 and int(actual)==status and (expected is None or actual_body==expected)
    results.append({'example':key,'method':method,'path':path,'request':body,'expectedStatus':status,'expectedBody':expected,'actualStatus':int(actual),'body':actual_body,'passed':passed})
  finally:
   command(['pkill','-f','^dotnet '+dll]);process.wait(timeout=5)
Path('/tmp/cstudy-existing-web-results.json').write_text(json.dumps(results,ensure_ascii=False,indent=2))
print('HTTP',len(results),'PASS',sum(r['passed'] for r in results))
for r in results:
 if not r['passed']:print(r)
