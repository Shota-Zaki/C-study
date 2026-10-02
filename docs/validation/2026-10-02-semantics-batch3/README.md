# Original semantic output 2026-10-02-semantics-batch3

Fixed input: `b27ba4c3b2abf30c3e147d9c7efddb6654741783`. Expectations established before execution from matching source and teaching text; expectations.json retains exact source/project/teaching SHA256, excerpts and reasoning. Original supplied inputs are checked, not every possible input or branch.

| Original | Complete output (line separators shown as /) | Teaching semantics |
| --- | --- | --- |
|original-01|C#の学習を始めます / 全32レッスン|WriteLine order and interpolation of32|
|original-02|Hello C#|Append order and ToString|
|original-10|3|positive Add changes private-set Count0→3|
|original-11|メール通知|runtime override dispatch to EmailNotice|
|original-13|1 / 9|struct copy independent; class references share state|
|original-16|C# / 整数として読めませんでした|StringReader first line; invalid integer caught as FormatException|
|original-17|結果: 8 / 12|lambda doubles4; closure observes updated factor3|
|original-18|ペン, ノート|filter price<=500, order ascending then select names|
|original-19|2,3,4 / 2,3 / 9|deferred query sees added4, materialized snapshot does not, sum9|
|original-20|Doing / 2件 / 30 / True|enum member name, tuple count/sum, nonblank extension|

Actual builds and full-output runs: 10/10 PASS, exact stdout/stderr/exitCode with CRLF/LF normalization only. results.json retains every build/run command and lifecycle create/copy/SDK/cleanup. No source defect found for the supplied inputs. Reviewer confirmation recorded below.

Harness verify.py is self-contained when placed here in the repository: it checks hashes before copying only selected sources into private temporary fixtures, builds/runs sequentially in one task-owned container with existing pinned image, no network,2CPU/2GB, cleared NuGet packageSources,120s build/15s run timeouts. No source-tree builds, host mounts or shared service changes. Cleanup exit0. Reproduction should use a unique task-owned container name; no image installation/pull.

Cumulative original coverage 20/35; remaining 15 originals and191 existing Console examples. CS07 stays IN_PROGRESS; prior additional62 Console/31HTTP assertions and browser/device acceptance remain separate. No main/deploy/source/security changes. Work checkpoint uses existing [skip publish] workflow guard.

Independent read-only review `review_batch2`:10/10 expectations, baseline source/project/HTML hashes, results and isolation approved; no blocking findings. Output does not prove unobservable disposal behavior. No reviewer Docker rerun.
