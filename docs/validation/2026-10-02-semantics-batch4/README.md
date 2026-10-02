# Original semantic output 2026-10-02-semantics-batch4

Fixed input: `b7b908bc9c8d9b5a8875710fb2afd44d00246787`. Expectations established before execution from matching source and teaching text; expectations.json retains exact source/project/teaching SHA256, excerpts and reasoning. Original supplied inputs are checked, not every possible input or branch.

| Original | Complete output (line separators shown as /) | Teaching semantics |
| --- | --- | --- |
|original-21|{"Subject":"CSharp","Minutes":30} / 30|serialize record fields then deserialize Minutes30|
|original-22|2026-09-14 00:00 UTC / 45分 / 1234.50|UTC conversion subtracts9h, duration45min, invariant decimal2digits|
|original-23|開始 / 読み込み結果 / 完了|await resumes before result and completion output|
|original-24|30 / キャンセルしました|WhenAll results10+20; pre-canceled token causes caught cancellation|
|original-25|.NET学習プロジェクト / System.String / 標準ライブラリだけで動作します|string alias resolves System.String; standard library only|
|original-26|3件の検証に成功|59 false/60 true/61 true assertions permit success output|
|original-27|合計: 1500|parse positive quantity3, price500→1500|
|original-28|80|local DemoHandler returns200JSON score80 without external network|

Actual builds and full-output runs: 8/8 PASS, exact stdout/stderr/exitCode with CRLF/LF normalization only. results.json retains every build/run command and lifecycle create/copy/SDK/cleanup. No source defect found for the supplied inputs. Reviewer confirmation recorded below.

Harness verify.py is self-contained when placed here in the repository: it checks hashes before copying only selected sources into private temporary fixtures, builds/runs sequentially in one task-owned container with existing pinned image, no network,2CPU/2GB, cleared NuGet packageSources,120s build/15s run timeouts. No source-tree builds, host mounts or shared service changes. Cleanup exit0. Reproduction should use a unique task-owned container name; no image installation/pull.

Cumulative original coverage 28/35; remaining 7 originals and191 existing Console examples. CS07 stays IN_PROGRESS; prior additional62 Console/31HTTP assertions and browser/device acceptance remain separate. No main/deploy/source/security changes. Work checkpoint uses existing [skip publish] workflow guard.

Independent read-only review `review_batch2`:8/8 source/teaching outputs, baseline hashes and logs approved, no blocking findings. Outputs do not establish timing/disposal/untested branches; original28 uses a local handler and makes no external connectivity claim. No reviewer Docker rerun.
