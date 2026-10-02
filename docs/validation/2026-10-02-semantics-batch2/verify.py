from pathlib import Path
import json,subprocess,hashlib
root=Path(__file__).resolve().parent
container='cstudy-semantic-task6-batch2-20261002'
image='sha256:35d40304542c8689331f8cab17c65926cdf48fe711e289321d71924b230a7d29'
results=[]
def run(args,timeout=120):
 p=subprocess.run(args,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=timeout)
 return {'command':args,'exitCode':p.returncode,'output':p.stdout}
try:
 create=run(['docker','run','-d','--pull=never','--name',container,'--network','none','--cpus','2','--memory','2g',image,'sleep','600'])
 assert create['exitCode']==0,create
 copy=run(['docker','cp',str(root)+'/.',container+':/verify'])
 assert copy['exitCode']==0,copy
 for entry in json.loads((root/'expectations.json').read_text()):
  n=entry['lesson'];path=f'/verify/samples/lesson-{n:02}/Lesson.csproj'
  build=run(['docker','exec',container,'dotnet','build',path,'--nologo','--disable-build-servers','--configfile','/verify/NuGet.Config'])
  assert build['exitCode']==0,build
  result=run(['docker','exec',container,'dotnet','run','--project',path,'--no-build'],15)
  passed=result['exitCode']==0 and result['output'].replace('\r\n','\n')==entry['expected']
  results.append({'lesson':n,'expected':entry['expected'],'build':build,'run':result,'semanticMatch':passed})
  (root/'results.json').write_text(json.dumps({'sourceSHA':'f8efc923436b89654fd082c015040fd030eadac0','image':image,'results':results},ensure_ascii=False,indent=2)+'\n')
  print(f'lesson-{n:02}: '+('PASS' if passed else 'FAIL'),flush=True)
  assert passed,result
finally:
 print(run(['docker','rm','-f',container],15))
