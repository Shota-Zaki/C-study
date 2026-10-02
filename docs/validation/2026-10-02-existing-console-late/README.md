# Existing Console semantic verification — 2026-10-02-existing-console-late

Fixed input `7bb393a6f7c68db07bec517b9a310ab2c393a3c6`. 36 unique existing Console examples, pre-established full stdout/exitCode/stderr expectations from matching Program.cs and canonical teaching sections. expectations.json retains source/project/teaching hashes, precise excerpts and reasoning; intentional runnable mistakes preserve their demonstrated outputs. Error/nonstandalone examples are not silently run as successful Console cases.

Actual 36/36 builds/runs and semantic contracts PASS. Full stdout/stderr compared with only CRLF/LF normalization, except an explicitly described dynamic timing contract if present. results.json preserves commands/logs/lifecycle SDK/runtime and cleanup exit0. One existing pinned-image container, no network,2CPU/2GB, private copied fixtures, per-example CWD, sequential build120s/run15s. Any stdin is piped without terminal echo; any file is in disposable per-example space. No host mounts, installs, source changes, services, main or deploy. verify.py reproduces from this repository with unique container name and existing image.

| Example | Expected complete stdout (line separators shown as /) | Semantics |
| --- | --- | --- |
|deep-21-01|{"Name":"Note","Quantity":3} / Note:3|JSON roundtrip preserves Name and Quantity; property order observed for these declared properties.|
|deep-21-02|作業場所:/verify/deep-21-02 / アプリ基準:/verify/deep-21-02/bin/Debug/net10.0/ / 保存先:/verify/deep-21-02/data/items.json|Working directory, application base and combined data path have independent meanings.|
|deep-21-03|Note:3 / Pen:2|Serializes two ordered records into a practice file and reloads their values.|
|deep-21-04|-5|Deliberately invalid business data still deserializes: negative quantity is observed, not repaired.|
|deep-21-05|名前と数量を確認してください|Business validation rejects blank name and negative quantity before use.|
|deep-21-06|未設定 / Note|Default JSON property matching is case sensitive; explicitly insensitive matching recognizes name.|
|deep-22-01|2026-09-30 / 2026-10-01|AddDays returns next date across month boundary.|
|deep-22-02|2026-09-14 09:00 +09:00 / 2026-09-14 00:00 +00:00 / True|Offset representations denote identical instant.|
|deep-22-03|Unspecified / Utc|Constructor Kind differs; no implicit regional time assumption.|
|deep-22-05|2026-09-14|Exact invariant date format parses successfully.|
|deep-22-06|残り6日|Fixed DayNumber subtraction avoids current-clock dependency.|
|deep-22-07|2026-09-14|Intentional discarded AddDays result leaves original value unchanged.|
|deep-22-08|2026-09-15|Assigning returned AddDays value advances date.|
|deep-22-09|\A4999950000\n計測ミリ秒:([0-9]+(?:\.[0-9]+)?(?:[Ee][+-]?[0-9]+)?)\n\Z|Sum is deterministic; elapsed Stopwatch milliseconds are runtime measurement.|
|deep-23-01|開始 / 受信完了 / 終了|Await keeps final output after asynchronous result.|
|deep-23-02|1:呼び出す前 / 2:最初のawaitより前 / 3:呼び出し元へ戻った / 4:信号の後に完了|Synchronous prefix precedes return; incomplete signal enforces later completion ordering.|
|deep-23-04|実際の保存処理が完了 / 保存できました|Await saves before claiming successful save.|
|deep-23-05|読み込み失敗:形式が不正です|Await observes async exception and typed handler prints failure.|
|deep-24-01|10,20|WhenAll results retain input task order.|
|deep-24-02|False / 10,20|Completing second task alone does not complete WhenAll; results follow input order.|
|deep-24-03|失敗件数:2|WhenAll stores both failures; aggregate count observed after await failure.|
|deep-24-04|中止しました|Pre-cancelled token throws before completion output; filtered handler recognizes cancellation.|
|deep-24-06|10,20,30,40|Semaphore bounds concurrent work while WhenAll output follows original input order.|
|deep-24-07|True|WhenAny chooses a completed task; chosen value can be either 10 or 20, boolean contract remains true.|
|deep-25-04|開始|Top-level executable statement prints before separate Product type declaration; not the multi-file 360 example.|
|deep-26-01|境界5000の比較が一致|At boundary 5000, inclusive free-shipping condition matches independent expected zero.|
|deep-26-02|500 / 500 / 0|Intentional exclusive-threshold defect exhibits incorrect boundary value, as lesson teaches.|
|deep-26-03|500 / 0 / 0|Repaired inclusive threshold matches below/at/above boundary outputs.|
|deep-26-05|4つの比較が一致|Four assertions check accepted take, remaining count, rejected take, unchanged rejected state.|
|deep-27-01|合計:360|Calculation returns checked 120 times 3 and presentation formats total.|
|deep-27-02|2個を受け付けました / 在庫不足です / 整数で入力してください / 最終在庫:3|Parse/business/presentation separation; accepted take reduces stock, rejected and malformed inputs do not.|
|deep-27-03|False / -2|Intentional mutation-before-validation defect corrupts stock despite rejection.|
|deep-27-04|False / 3|Validation before mutation preserves rejected stock.|
|deep-28-01|要求:GET /items/3 / 200 / Note|In-memory handler observes GET path, returns successful HTTP response and JSON DTO; no actual external network.|
|deep-28-03|対象がありません|404 branch bypasses success DTO parsing.|
|deep-31-01|UTC年:2026|Injected fixed clock makes greeting independent of present date.|

Cumulative existing Console coverage159/193 (191 ordinary+1stdin+1file); remaining34. Originals35/35 have separate selected-input/HTTP evidence. No blanket branch/input/platform guarantee. CS07 remains IN_PROGRESS; UI/browser/device acceptance separate. Work push uses existing [skip publish] guard.

Special contracts: deep21-02 exact predetermined private CWD/base/save paths, deep21-03 full stdout plus ordered persisted JSON records, deep22-09 exact sum4999950000 and anchored finite nonnegative elapsed-milliseconds field. Runtime LANG=C/LC_ALL=C pins numeric formatting while explicit CultureInfo remains available; no global invariant mode or performance claim. Intentional swallowed-file/rounding/constant-test/output-order mistakes preserve taught outputs.

Independent read-only reviewer console_expectations_middle approved all36 contracts, current hashes, full final outputs/file JSON/timing constraint and lifecycle. No defects or blockers; no Docker rerun.
