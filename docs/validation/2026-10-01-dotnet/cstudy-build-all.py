import concurrent.futures,json,subprocess,time
from pathlib import Path
root=Path('/tmp/cstudy-validation-path').read_text()
paths=sorted(str(p.relative_to(root)) for p in Path(root).rglob('*.csproj'))
def build(path):
 result=subprocess.run(['docker','exec','cstudy-sdk-20261001','dotnet','build',path,'--nologo','--disable-build-servers'],capture_output=True,text=True,timeout=120)
 return {'project':path,'exitCode':result.returncode,'output':result.stdout+result.stderr}
results=[]
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
 for result in pool.map(build,paths):
  results.append(result)
  print(len(results),result['project'],result['exitCode'],flush=True)
  Path('/tmp/cstudy-build-results.json').write_text(json.dumps(results,ensure_ascii=False,indent=2))
print('TOTAL',len(results),'FAIL',sum(r['exitCode']!=0 for r in results),flush=True)
