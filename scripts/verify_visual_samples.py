#!/usr/bin/env python3
"""Build the 64 new C# sample projects only after an explicit --build.
Does not install an SDK or execute user code. Exit: 0 built; 1 failed; 2 unverified.
"""
from __future__ import annotations
import argparse, datetime, json, shutil, subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / 'validation/visual/dotnet-new-samples.json'


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--build', action='store_true')
    args = parser.parse_args()
    entries = json.loads((ROOT / 'content/visual/sample-manifest.json').read_text(encoding='utf-8'))
    sdk = shutil.which('dotnet')
    report = {
        'date': datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'target': '.NET 10 / C# 14', 'projects': len(entries), 'sdkPath': sdk,
        'status': 'UNVERIFIED', 'builds': [],
        'execution': 'NOT_PERFORMED',
        'expectedOutputs': 'Not compared with observed output',
    }
    def save() -> None:
        REPORT.parent.mkdir(parents=True, exist_ok=True)
        REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    if not sdk:
        report['reason'] = '.NET SDK command is unavailable. No compilation or execution occurred.'
        save(); print('UNVERIFIED: .NET SDK unavailable.'); return 2
    if not args.build:
        report['reason'] = '--build was not requested.'
        save(); print('UNVERIFIED: pass --build to compile the samples.'); return 2
    for entry in entries:
        project = (ROOT / entry['path'] / 'Example.csproj').resolve()
        if not project.is_relative_to(ROOT) or not project.is_file():
            raise ValueError(f'Invalid project path: {entry["path"]}')
        result = {'lesson': entry['lesson'], 'case': entry['case'], 'project': str(project.relative_to(ROOT))}
        try:
            run = subprocess.run([sdk, 'build', str(project), '--nologo'], cwd=ROOT,
                                 capture_output=True, text=True, encoding='utf-8', errors='replace',
                                 timeout=120, check=False)
            result.update(exitCode=run.returncode, output=run.stdout + run.stderr,
                          status='PASS' if run.returncode == 0 else 'FAIL')
        except (subprocess.TimeoutExpired, OSError) as exc:
            result.update(status='FAIL', reason=str(exc))
        report['builds'].append(result)
        print(entry['lesson'], entry['case'], result['status'], flush=True)
        save()
    passed = all(item['status'] == 'PASS' for item in report['builds']) and len(report['builds']) == len(entries)
    report['status'] = 'BUILD_COMMANDS_SUCCEEDED' if passed else 'FAIL'
    save()
    return 0 if passed else 1


if __name__ == '__main__':
    raise SystemExit(main())
