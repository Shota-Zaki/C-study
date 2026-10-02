# Existing Console semantic verification — 2026-10-02-existing-console-early

Fixed input `5aa116852eee28c046356eeb8e751796857db908`. 47 unique existing Console examples, pre-established full stdout/exitCode/stderr expectations from matching Program.cs and canonical teaching sections. expectations.json retains source/project/teaching hashes, precise excerpts and reasoning; intentional runnable mistakes preserve their demonstrated outputs. Error/nonstandalone examples are not silently run as successful Console cases.

Actual 47/47 builds/runs and semantic contracts PASS. Full stdout/stderr compared with only CRLF/LF normalization, except an explicitly described dynamic timing contract if present. results.json preserves commands/logs/lifecycle SDK/runtime and cleanup exit0. One existing pinned-image container, no network,2CPU/2GB, private copied fixtures, per-example CWD, sequential build120s/run15s. Any stdin is piped without terminal echo; any file is in disposable per-example space. No host mounts, installs, source changes, services, main or deploy. verify.py reproduces from this repository with unique container name and existing image.

| Example | Expected complete stdout (line separators shown as /) | Semantics |
| --- | --- | --- |
|deep-01-01|学習開始 / 30 / 30|total stores20+10 and is unchanged by later minutes50|
|deep-01-02|合計: 65分 / 目標まで: 25分|25+40=65;90-65=25|
|deep-01-04|学習開始 / 20|sequential literal then variable output|
|deep-01-05|90|recompute total after minutes80|
|deep-02-01|入口 / 呼び出された処理 / 終了|top-level call returns before final output|
|deep-02-02|入口 / 呼び出された処理 / 終了|Main has same call order|
|deep-02-03|在庫の商品 / 注文の商品|aliases resolve two distinct namespace Product types|
|deep-02-05|開始|top-level statement precedes type declaration repaired example|
|deep-02-07|在庫|fully qualified Inventory.Product resolves namespace|
|deep-03-01|360|3*120|
|deep-03-02|在庫: 3 / True|var inferred int/string/decimal; equality decimal true|
|deep-03-04|3個|interpolate inferred int3 into string|
|deep-03-05|True / True|int division5/2=2 assigned double; cast before division2.5|
|deep-03-06|595.5 / 60 / 655.5|198.5*3=595.5;round59.55→60; invariant formats|
|deep-03-07|intの範囲を超えました|checked max+1 caught OverflowException|
|deep-04-01|[  C#  ] / [C#] / 6 / 2|Trim returns new string, original6 UTF16 units and trimmed2|
|deep-04-02|True / 25|TryParse25 success with out25|
|deep-04-03|数量を入力: 合計: 360円|stdin3 passes parse/range; Write prompt has no newline and pipe has no echo|
|deep-04-05|数量の形式が正しくありません|abc fails TryParse and uses else|
|deep-04-06|[  Aoi  ]|discarded Trim return leaves immutable string unchanged; intentional wrong example|
|deep-04-07|[Aoi]|assign returned trimmed string|
|deep-04-08|84|TryParse accepts leading/trailing whitespace;42*2|
|deep-05-01|合格・優秀 / 判定終了|80 chooses first >=80; common continuation|
|deep-05-02|False|short circuit false guard avoids divide by zero|
|deep-05-03|料金: 500円|age12 valid then6<=age<18|
|deep-05-04|通常合格|intentional wrong condition order:90 first matches>=60|
|deep-05-05|優秀合格|corrected descending threshold order|
|deep-05-06|合格|75 first matching switch arm>=60|
|deep-06-01|20 / 40 / 3|read element0, update1, Length3|
|deep-06-02|i=0, total=20 / i=1, total=55 / i=2, total=70 / 合計=70|for accumulator20→55→70|
|deep-06-03|70|foreach20+35+15|
|deep-06-04|学習日=4 / 合計=105|skip0;20+45+10+30 and count4|
|deep-06-06|10 / 20 / 30|fixed strict <Length avoids out of range|
|deep-06-08|0 / 2|continue skips1; for increment still happens|
|deep-06-09|件数=3, 合計=230|scores>=60 are80,60,90|
|deep-07-01|360|method120*3 return|
|deep-07-02|15 / 10|callee modifies copy and prints15; caller10 unchanged|
|deep-07-03|15|caller assigns returned value|
|deep-07-04|7,8 / 9,2|array object mutation shared; parameter reassign local only|
|deep-07-05|6 / True, 12|ref increments caller;out parses12|
|deep-07-06|小計=550, 支払=500|sum120+250+180=550 discount50|
|deep-08-01|名前がありません|null branch prevents member access|
|deep-08-02|False / 0 / 未登録|conditional access produces nullable without value, coalescing fallbacks|
|deep-08-03|匿名 / 匿名 / 匿名 / Aoi|null empty whitespace fallback; trim valid name|
|deep-08-05|0|null conditional+fallback0|
|deep-08-07|未受験|nullable score null does not match int pattern|
|deep-08-08|未受験 / 0点 / 80点|null distinguished from valid0 and80|

Cumulative existing Console coverage47/193 (191 ordinary+1stdin+1file); remaining146. Originals35/35 have separate selected-input/HTTP evidence. No blanket branch/input/platform guarantee. CS07 remains IN_PROGRESS; UI/browser/device acceptance separate. Work push uses existing [skip publish] guard.

Independent read-only reviewer review_batch2 approved47/47 source/teaching/hash contracts and final full-output/lifecycle results; no defects/blockers, no Docker rerun. stdin3 prompt has no newline/echo, correctly shares result line. Intentional mistake/repair outputs preserved.
