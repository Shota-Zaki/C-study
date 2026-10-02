"""Run fixed semantic expectations in private copied fixtures and one isolated container."""
from pathlib import Path
import json,subprocess,hashlib,tempfile,shutil,time
from cases import cases
root=Path(__file__).resolve().parent
repo=root.parents[2]
image='sha256:35d40304542c8689331f8cab17c65926cdf48fe711e289321d71924b230a7d29'
container='cstudy-task6-'+root.name
report={'sourceSHA':subprocess.check_output(['git','-C',str(repo),'rev-parse','HEAD'],text=True).strip(),'image':image,'lifecycle':{},'results':[]}
def run(args,timeout=120):
 p=subprocess.run(args,text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=timeout)
 return {'command':args,'exitCode':p.returncode,'stdout':p.stdout,'stderr':p.stderr}
def save(): (root/'results.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
try:
 with tempfile.TemporaryDirectory(prefix='cstudy-private-') as tmp:
  tmp=Path(tmp);(tmp/'NuGet.Config').write_text('<configuration><packageSources><clear /></packageSources></configuration>\n')
  entries=json.loads((root/'expectations.json').read_text())
  for e in entries:
   src=repo/e['source']
   for f,h in e['sha256'].items(): assert hashlib.sha256((src/f).read_bytes()).hexdigest()==h,(e['id'],f)
   assert hashlib.sha256((repo/e['teachingPath']).read_bytes()).hexdigest()==e['teachingSha256'],e['id']
   shutil.copytree(src,tmp/e['id'])
  report['lifecycle']['create']=run(['docker','run','-d','--pull=never','--name',container,'--network','none','--cpus','2','--memory','2g',image,'sleep','900']);save()
  assert report['lifecycle']['create']['exitCode']==0
  report['lifecycle']['copy']=run(['docker','cp',str(tmp)+'/.',container+':/verify']);save();assert report['lifecycle']['copy']['exitCode']==0
  report['lifecycle']['sdk']=run(['docker','exec',container,'dotnet','--info']);save()
  for e in entries:
   project=f"/verify/{e['id']}/{e['project']}"
   build=run(['docker','exec',container,'dotnet','build',project,'--nologo','--disable-build-servers','--configfile','/verify/NuGet.Config'])
   assert build['exitCode']==0,build
   dll=project.rsplit('/',1)[0]+'/bin/Debug/net10.0/'+Path(e['project']).stem+'.dll'
   log=root/(e['id']+'-server.log')
   with log.open('w') as output:
    proc=subprocess.Popen(['docker','exec',container,'dotnet',dll],stdout=output,stderr=subprocess.STDOUT)
    try:
     for attempt in range(50):
      ready=run(['docker','exec',container,'curl','-s','--max-time','1','http://127.0.0.1:5080/__readiness'],3)
      if ready['exitCode']==0:break
      time.sleep(.1)
     else:raise RuntimeError('server not ready')
     checks=[]
     for method,path,body,status,expected in cases(e['id']):
      args=['docker','exec',container,'curl','-sS','--max-time','3','-D','-','-X',method]
      if body is not None:args+=['-H','Content-Type: application/json','--data',json.dumps(body,ensure_ascii=False)]
      args+=['http://127.0.0.1:5080'+path]
      result=run(args,5);raw=result['stdout'];headers,actual=raw.split('\r\n\r\n' if '\r\n\r\n' in raw else '\n\n',1)
      actualStatus=int(headers.splitlines()[0].split()[1]);actualBody=json.loads(actual) if actual else None
      passed=result['exitCode']==0 and actualStatus==status and actualBody==expected
      if status==201:passed=passed and ('Location: /tasks/'+str(actualBody['id'])) in headers
      check={'method':method,'path':path,'request':body,'expectedStatus':status,'expectedBody':expected,'response':result,'actualStatus':actualStatus,'actualBody':actualBody,'semanticMatch':passed};checks.append(check)
      report['results'].append({'id':e['id'],'build':build,'check':check,'semanticMatch':passed});save();assert passed,check
     print(e['id']+': '+str(len(checks))+' HTTP PASS',flush=True)
    finally:
     stopped=run(['docker','exec',container,'pkill','-f',dll],5)
     proc.wait(timeout=10);report['lifecycle'][e['id']+'Stop']=stopped;save()

finally:
 report['lifecycle']['cleanup']=run(['docker','rm','-f',container],15);save();print('cleanup:',report['lifecycle']['cleanup']['exitCode'],flush=True)
