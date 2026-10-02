# Existing Console semantic verification — 2026-10-02-existing-console-guides

Fixed input `7bb393a6f7c68db07bec517b9a310ab2c393a3c6`. 34 unique existing Console examples, pre-established full stdout/exitCode/stderr expectations from matching Program.cs and canonical teaching sections. expectations.json retains source/project/teaching hashes, precise excerpts and reasoning; intentional runnable mistakes preserve their demonstrated outputs. Error/nonstandalone examples are not silently run as successful Console cases.

Actual 34/34 builds/runs and semantic contracts PASS. Full stdout/stderr compared with only CRLF/LF normalization, except an explicitly described dynamic timing contract if present. results.json preserves commands/logs/lifecycle SDK/runtime and cleanup exit0. One existing pinned-image container, no network,2CPU/2GB, private copied fixtures, per-example CWD, sequential build120s/run15s. Any stdin is piped without terminal echo; any file is in disposable per-example space. No host mounts, installs, source changes, services, main or deploy. verify.py reproduces from this repository with unique container name and existing image.

| Example | Expected complete stdout (line separators shown as /) | Semantics |
| --- | --- | --- |
|guides-learning-workflow-01|残り3回|Four planned sessions minus one completed session leaves three.|
|guides-runtime-memory-01|10 / 15|Value parameter modification leaves caller total at 10 and returns 15.|
|guides-runtime-memory-02|3/9 / 3,9|Integer copy changes separately; both List references observe added 9.|
|guides-runtime-memory-03|本,ペン|Struct copy shares its contained List reference.|
|guides-runtime-memory-04|一行目 / 二行目 / 読み取り終了|Read two StringReader lines, dispose at using boundary, then print completion.|
|guides-reading-code-01|340|120*3=360 meets discount condition and subtracts 20.|
|guides-reading-code-02|開始 / 計算中 / 5 / 終了|Method body executes at call and returns 5 before caller continues.|
|guides-reading-code-03|0,1,2|Read index before each explicit increment.|
|guides-reading-code-05|0|50 fails >=60; both conditional statements are skipped.|
|guides-errors-02|4|TryParse succeeds for string 3 then adds one.|
|guides-errors-03|True|Intentional integer-division demonstration truncates 5/2 to 2 before double conversion.|
|guides-errors-04|True|Cast before division computes 2.5 and comparison succeeds.|
|guides-errors-06|名前が未指定です|Null guard prints missing-name branch without dereference.|
|guides-errors-08|10 / 20 / 30|Strict less-than length visits array indices 0,1,2 only.|
|guides-errors-10|0 / 2|For update advances index despite continue at 1.|
|guides-errors-11|3|Intentional aliasing demonstration: backup shares original List.|
|guides-errors-12|2|Copy constructor creates independent List before original is changed.|
|guides-errors-14|3|Instance method reads its Counter instance value.|
|guides-errors-16|True / 3|Valid withdrawal 2 from stock 5 succeeds and leaves 3.|
|guides-errors-17|False|Ordinary class instances compare unequal by reference identity.|
|guides-errors-18|True / False|Record values compare equal while separate instances have distinct references.|
|guides-errors-19|2,3|Deferred Where enumeration sees added 3.|
|guides-errors-20|2|ToList materializes matching values before added 3.|
|guides-errors-22|保存相当の処理が完了 / メイン終了|Await observes task completion before main completion message.|
|guides-errors-24|保存に失敗しました。入力は保持します。 / False|Caught IO failure prints failure and does not change saved to true.|
|guides-choosing-features-01|2,3 / 5,3 / True|With produces changed value without altering first and generated value equality succeeds.|
|guides-choosing-features-02|ペン / True / False|Dictionary key 20 resolves pen; HashSet first addition succeeds and duplicate fails.|
|guides-choosing-features-03|8|Ref parameter assignment changes caller variable.|
|guides-async-timeline-01|1:呼び出し前 / 2:待機の直前 / 3:まだ合図していない / 4:結果は7 / 5:観察が完了|Incomplete task suspends observer; explicit signal supplies 7; awaiting observer orders final message after result.|
|guides-async-timeline-02|False / 10,20|WhenAll remains incomplete until both finish and returns results in supplied task order.|
|guides-async-timeline-03|処理の失敗を受け取りました|Await receives failed task exception and matching catch prints handling message.|
|guides-async-timeline-04|中止されました|Already cancelled token cancels Delay and matching catch prints cancellation.|
|guides-http-di-path-01|1:学習:False|Trim accepts title and creates fixed ID 1 with incomplete status; no HTTP or persistence occurs.|
|guides-http-di-path-02|こんにちは、学習者|Constructor-injected fixed name source supplies greeting without network.|

Cumulative existing Console coverage193/193 (191 ordinary+1stdin+1file); remaining0. Originals35/35 have separate selected-input/HTTP evidence. No blanket branch/input/platform guarantee. CS07 remains IN_PROGRESS; UI/browser/device acceptance separate. Work push uses existing [skip publish] guard.

Independent read-only reviewer console_expectations_late approved34/34 pre-runtime source/teaching/hash contracts and final complete-output/build/lifecycle results. No defects/blockers; no Docker rerun.
