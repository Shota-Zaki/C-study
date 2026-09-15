#!/usr/bin/env python3
"""Copy generated public pages and their dependencies into an empty directory.
Never deletes existing files, never uploads or modifies a remote repository.
"""
from __future__ import annotations
import argparse, json, shutil
from pathlib import Path
from urllib.parse import unquote, urlsplit
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]


def public_files() -> list[Path]:
    htmls = sorted([*ROOT.glob('*.html'), *(ROOT/'lessons').glob('*.html'),
                   *(ROOT/'deep-dives').glob('*.html'), *(ROOT/'guides').glob('*.html'),
                   *(ROOT/'projects').glob('*.html')])
    files = set(htmls)
    files.update(path for path in (ROOT/'assets').rglob('*') if path.is_file())
    files.update(path for path in (ROOT/'samples/visual').rglob('*') if path.is_file())
    files.update(ROOT/name for name in ('.nojekyll', 'robots.txt') if (ROOT/name).is_file())
    for page in htmls:
        soup = BeautifulSoup(page.read_text(encoding='utf-8'), 'html.parser')
        for element in soup.select('[href], [src]'):
            for attr in ('href', 'src'):
                if not element.has_attr(attr):
                    continue
                url = urlsplit(element[attr])
                if url.scheme or url.netloc or not url.path:
                    continue
                target = (page.parent/unquote(url.path)).resolve()
                if url.path.endswith('/'):
                    target /= 'index.html'
                if not target.is_relative_to(ROOT) or not target.is_file():
                    raise ValueError(f'Invalid local dependency: {page.relative_to(ROOT)} -> {element[attr]}')
                files.add(target)
    return sorted(files)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    output = args.output.resolve()
    if output == ROOT or ROOT.is_relative_to(output):
        parser.error('The output must not be the source directory or an ancestor of it.')
    if output.exists() and (not output.is_dir() or any(output.iterdir())):
        parser.error('The output directory must be absent or empty. No files were deleted.')
    files = public_files()
    output.mkdir(parents=True, exist_ok=True)
    for path in files:
        target = output/path.relative_to(ROOT)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, target)
    largest = max(files, key=lambda p: p.stat().st_size)
    report = {'files': len(files), 'uncompressedBytes': sum(p.stat().st_size for p in files),
              'largestFile': str(largest.relative_to(ROOT)), 'largestFileBytes': largest.stat().st_size,
              'rootEntry': 'index.html', 'serverFunctions': False, 'browserCSharpRunner': False}
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
