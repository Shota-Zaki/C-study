#!/usr/bin/env python3
"""Lexical sanity audit for C# examples.

This is intentionally not a compiler. It catches migration/regression defects such as
ordinary-string newlines, unterminated strings/comments, and unbalanced (), [] or {}.
Use build_samples.sh with a real .NET SDK for authoritative compilation.
"""
from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
COURSE = json.loads((ROOT / 'content/course.json').read_text(encoding='utf-8'))
PROJECTS = json.loads((ROOT / 'content/projects.json').read_text(encoding='utf-8'))


def scan(code: str):
    issues = []
    stack = []
    pairs = {')': '(', ']': '[', '}': '{'}
    i = 0
    line = 1
    n = len(code)
    state = 'normal'
    quote_count = 0

    def escaped(pos):
        count = 0
        pos -= 1
        while pos >= 0 and code[pos] == '\\':
            count += 1
            pos -= 1
        return count % 2 == 1

    while i < n:
        ch = code[i]
        nxt = code[i + 1] if i + 1 < n else ''

        if state == 'line_comment':
            if ch == '\n':
                line += 1
                state = 'normal'
            i += 1
            continue

        if state == 'block_comment':
            if ch == '*' and nxt == '/':
                state = 'normal'
                i += 2
                continue
            if ch == '\n':
                line += 1
            i += 1
            continue

        if state == 'regular_string':
            if ch == '\n':
                issues.append(f'line {line}: newline inside ordinary string literal')
                line += 1
                state = 'normal'
                i += 1
                continue
            if ch == '"' and not escaped(i):
                state = 'normal'
            i += 1
            continue

        if state == 'verbatim_string':
            if ch == '"':
                if nxt == '"':
                    i += 2
                    continue
                state = 'normal'
                i += 1
                continue
            if ch == '\n':
                line += 1
            i += 1
            continue

        if state == 'raw_string':
            if ch == '"':
                run = 1
                while i + run < n and code[i + run] == '"':
                    run += 1
                if run >= quote_count:
                    state = 'normal'
                    i += quote_count
                    continue
            if ch == '\n':
                line += 1
            i += 1
            continue

        if state == 'char':
            if ch == '\n':
                issues.append(f'line {line}: newline inside character literal')
                line += 1
                state = 'normal'
                i += 1
                continue
            if ch == "'" and not escaped(i):
                state = 'normal'
            i += 1
            continue

        # normal state
        if ch == '/' and nxt == '/':
            state = 'line_comment'
            i += 2
            continue
        if ch == '/' and nxt == '*':
            state = 'block_comment'
            i += 2
            continue
        if ch == '\n':
            line += 1
            i += 1
            continue
        if ch == "'":
            state = 'char'
            i += 1
            continue
        if ch == '"':
            run = 1
            while i + run < n and code[i + run] == '"':
                run += 1
            if run >= 3:
                quote_count = run
                state = 'raw_string'
                i += run
                continue
            # Verbatim string prefix can be @" or $@" / @$".
            prev = code[max(0, i - 2):i]
            if (i > 0 and code[i - 1] == '@') or prev in ('$@', '@$'):
                state = 'verbatim_string'
            else:
                state = 'regular_string'
            i += 1
            continue
        if ch in '([{':
            stack.append((ch, line))
        elif ch in ')]}':
            if not stack or stack[-1][0] != pairs[ch]:
                issues.append(f'line {line}: unmatched {ch}')
            else:
                stack.pop()
        i += 1

    if state == 'block_comment':
        issues.append(f'line {line}: unterminated block comment')
    elif state in {'regular_string', 'verbatim_string', 'raw_string'}:
        issues.append(f'line {line}: unterminated string literal')
    elif state == 'char':
        issues.append(f'line {line}: unterminated character literal')
    for opener, opener_line in reversed(stack):
        issues.append(f'line {opener_line}: unclosed {opener}')
    return issues


snippets = []
for lesson in COURSE['lessons']:
    lid = lesson['id']
    snippets.extend([
        (f'L{lid} example', lesson['example']),
        (f'L{lid} worked-flow', lesson['deep']['walk']['code']),
        (f'L{lid} repaired-code', lesson['deep']['bug']['after']),
        (f'L{lid} focus-code', lesson['csharp_focus']['code']),
        (f'L{lid} basic-solution', lesson['exercise']['solution']),
    ])
    for idx, drill in enumerate(lesson['deep']['drills'], 1):
        snippets.append((f'L{lid} drill-{idx}-solution', drill['solution']))
for project in PROJECTS:
    snippets.append((f'project {project["id"]}', project['code']))

sample_files = sorted((ROOT / 'samples').rglob('*.cs'))
for path in sample_files:
    snippets.append((f'file {path.relative_to(ROOT)}', path.read_text(encoding='utf-8')))

failures = []
for label, code in snippets:
    for issue in scan(code):
        failures.append((label, issue))

report = {
    'kind': 'lexical-sanity-not-compilation',
    'snippets': len(snippets),
    'course_snippets': len(snippets) - len(sample_files),
    'sample_files': len(sample_files),
    'failures': [{'label': label, 'issue': issue} for label, issue in failures],
}
(ROOT / 'docs/csharp_static_audit.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(f'snippets={len(snippets)} sample_files={len(sample_files)} fail={len(failures)}')
for label, issue in failures[:50]:
    print('FAIL', label, issue)
raise SystemExit(1 if failures else 0)
