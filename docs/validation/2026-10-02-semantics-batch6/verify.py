"""Run fixed semantic expectations in private copied fixtures and one isolated container."""
from pathlib import Path
import json,subprocess,hashlib,tempfile,shutil,re,uuid
from cases import expense_cases
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
   dll=project.rsplit('/',1)[0]+'/bin/Debug/net10.0/Project.dll'
   data='/verify/private-data';path=data+'/CSharpLearningLab/tasks.json'
   setup=run(['docker','exec',container,'mkdir','-p',data]);assert setup['exitCode']==0
   def invoke(args):return run(['docker','exec','-e','XDG_DATA_HOME='+data,container,'dotnet',dll,*args],15)
   def check(args,exitCode,stdout,stderr=''):
    result=invoke(args);passed=result['exitCode']==exitCode and result['stdout'].replace('\r\n','\n')==stdout and result['stderr'].replace('\r\n','\n')==stderr
    report['results'].append({'id':e['id'],'args':args,'expectedExitCode':exitCode,'expectedStdout':stdout,'expectedStderr':stderr,'build':build,'run':result,'semanticMatch':passed});save();assert passed,result
   if e['id']=='project-expense-cli':
    for args,code,stdout,stderr in expense_cases():check(args,code,stdout,stderr)
   else:
    check([],0,'コマンド: list / add "タイトル" / done ID / delete ID / where\n')
    check(['where'],0,path+'\n')
    check(['list'],0,'0件 / 完了0件\n')
    result=invoke(['add','  Learn CSharp  ']);match=re.fullmatch(r'追加: ([0-9a-f-]{36}) Learn CSharp\n',result['stdout']);passed=result['exitCode']==0 and not result['stderr'] and bool(match)
    assert passed,result
    ident=match.group(1);assert str(uuid.UUID(ident))==ident and uuid.UUID(ident).version==4
    report['results'].append({'id':e['id'],'args':['add','  Learn CSharp  '],'expectedPattern':'追加: <generated canonical UUIDv4> Learn CSharp\n','run':result,'semanticMatch':True});save()
    snapshot=run(['docker','exec',container,'cat',path]);items=json.loads(snapshot['stdout']);assert len(items)==1 and items[0]['Id']==ident and items[0]['Title']=='Learn CSharp' and items[0]['Done'] is False and items[0]['CreatedAt']
    report['lifecycle']['addedFile']=snapshot;save()
    check(['list'],0,'[ ] '+ident+' Learn CSharp\n1件 / 完了0件\n')
    check(['done',ident],0,'完了にしました。\n')
    check(['done',ident],0,'完了にしました。\n')
    check(['list'],0,'[x] '+ident+' Learn CSharp\n1件 / 完了1件\n')
    check(['delete',ident],0,'削除しました。\n')
    check(['list'],0,'0件 / 完了0件\n')
    check(['add','   '],1,'','処理を中断しました: タイトルは1〜100文字。空白を含む場合は引用符で囲んでください。\n保存先: '+path+'\n')
    check(['done','invalid'],1,'','処理を中断しました: listに表示された有効なIDを指定してください。\n保存先: '+path+'\n')
    check(['delete',ident],1,'','処理を中断しました: 対象のタスクがありません。\n保存先: '+path+'\n')
    check(['unknown'],1,'','不明なコマンドです。引数なしで使い方を表示します。\n')
    # Only synthetic disposable data is corrupted. Semantic JSON-null error is runtime-stable.
    bad=tmp/'invalid.json';bad.write_text('null');copied=run(['docker','cp',str(bad),container+':'+path]);assert copied['exitCode']==0
    before=run(['docker','exec',container,'cat',path])
    check(['add','Preserve'],1,'','処理を中断しました: 保存データがnullです。初期化せず中断します。\n保存先: '+path+'\n')
    after=run(['docker','exec',container,'cat',path]);assert before['stdout']==after['stdout']=='null'
    report['lifecycle']['corruptionPreserved']={'before':before,'after':after,'passed':True};save()
   print(e['id']+': PASS',flush=True)

finally:
 report['lifecycle']['cleanup']=run(['docker','rm','-f',container],15);save();print('cleanup:',report['lifecycle']['cleanup']['exitCode'],flush=True)
