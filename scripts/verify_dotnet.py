#!/usr/bin/env python3
"""Build explicitly requested samples and optionally run one reviewed console example.
No SDK download, no arbitrary shell execution, and no browser-side C# execution.
A compiler exit code is not a claim that the lesson's business requirements are correct.
"""
from __future__ import annotations
import argparse,json,shutil,subprocess,sys,datetime
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
REPORT=ROOT/'docs/validation/dotnet.json'

def command(args:list[str],timeout:int=120)->dict:
 try:
  completed=subprocess.run(args,cwd=ROOT,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=timeout,check=False)
  return {'command':args,'exitCode':completed.returncode,'output':completed.stdout,'status':'COMPLETED'}
 except subprocess.TimeoutExpired as error:
  text=error.stdout or ''
  if isinstance(text,bytes):text=text.decode(errors='replace')
  return {'command':args,'status':'TIMEOUT','output':text}
 except OSError as error:return {'command':args,'status':'UNVERIFIED','error':str(error)}

def main()->int:
 parser=argparse.ArgumentParser(description=__doc__)
 parser.add_argument('--build',action='store_true',help='Build every independent project in the manifest.')
 parser.add_argument('--run-id',help='Build and run this manifest ID only. Only csharp console examples are eligible; read the code first.')
 args=parser.parse_args();manifest=json.loads((ROOT/'samples/manifest.json').read_text());sdk=shutil.which('dotnet')
 report={'date':datetime.datetime.now(datetime.timezone.utc).isoformat(),'target':manifest['target'],'sdkPath':sdk,'projectsInManifest':sum(bool(e['project']) for e in manifest['entries']),'builds':[],'runs':[],'status':'UNVERIFIED'}
 if not sdk:
  report['reason']='dotnet command is unavailable. No compilation or execution occurred.'
  report['attempt']=command(['dotnet','--info'])
  REPORT.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print('UNVERIFIED: .NET SDK is unavailable.');return 2
 report['environment']=command([sdk,'--info'])
 if not args.build and not args.run_id:
  report['reason']='SDK information only; --build or --run-id is required.'
  REPORT.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print('SDK inspected; no build requested.');return 2
 selected=[e for e in manifest['entries'] if e['project']]
 if args.run_id:
  selected=[e for e in selected if e['id']==args.run_id]
  if not selected or selected[0]['kind']!='csharp':parser.error('--run-id must identify a standalone csharp console example, not a server/input/file/intentional error.')
 for entry in selected:
  project=(ROOT/entry['project']).resolve()
  if not project.is_relative_to(ROOT):raise ValueError('Manifest path escapes the package.')
  result=command([sdk,'build',str(project),'--nologo'],timeout=120);result['id']=entry['id'];result['project']=entry['project'];report['builds'].append(result)
  print(entry['id'],result['status'],result.get('exitCode',''),flush=True)
  if args.run_id and result.get('exitCode')==0:
   run=command([sdk,'run','--project',str(project),'--no-build'],timeout=15);run['id']=entry['id'];run['note']='Observed process output; compare it with the lesson. Exit code alone does not verify intended behavior.';report['runs'].append(run)
  REPORT.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
 failures=[r for r in report['builds']+report['runs'] if r.get('exitCode')!=0]
 report['status']='BUILD_COMMANDS_SUCCEEDED' if not failures else 'CHECK_REQUIRED'
 report['semanticValidation']='NOT_AUTOMATICALLY_PERFORMED'
 REPORT.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');return 0 if not failures else 1

if __name__=='__main__':raise SystemExit(main())
