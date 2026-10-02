"""Run fixed semantic expectations in private copied fixtures and one isolated container."""
from pathlib import Path
import json,subprocess,hashlib,tempfile,shutil
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
   result=run(['docker','exec',container,'dotnet','run','--project',project,'--no-build','--',*e['args']],15)
   passed=result['exitCode']==e['exitCode'] and result['stdout'].replace('\r\n','\n')==e['expected'] and result['stderr'].replace('\r\n','\n')==e.get('expectedStderr','')
   report['results'].append({'id':e['id'],'expected':e['expected'],'build':build,'run':result,'semanticMatch':passed});save()
   print(e['id']+': '+('PASS' if passed else 'FAIL'),flush=True)
   assert passed,result
finally:
 report['lifecycle']['cleanup']=run(['docker','rm','-f',container],15);save();print('cleanup:',report['lifecycle']['cleanup']['exitCode'],flush=True)
