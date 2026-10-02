# Original semantic output batch 2 — 2026-10-02

Fixed input: `f8efc923436b89654fd082c015040fd030eadac0`; shared checkout clean and remote work confirmed equal before testing. Remote main: `9e2ba2fea70e4748aa1991efb326555322b1d8c7`. Isolated local clone; no source changes.

Expected outputs were established before execution from the original Program.cs and matching rendered lesson 想定出力/処理順 (lesson05 uses its switch example, not the preceding shipping example). expectations.json retains source/project/lesson SHA256 and teaching excerpts.

| Original | Complete output (lines separated by /) | Teaching semantics |
| --- | --- | --- |
|03|2400 / 3 / 3.5|decimal multiplication, integer division truncation, floating division|
|04|今月は24時間学習 / True|Trim, successful TryParse, nonnegative hours, string content equality|
|05|よくできました|82 skips range error and selects first matching >=80 arm; no later arm output|
|06|人数: 3 / 合計: 245|three elements; accumulation 70→155→245|
|08|0 / 6 / -1|null-conditional/coalescing, nonnull length, nullable fallback|
|09|ざきです。C#を学習中です。|constructor initializes Name; instance method uses that state|

Actual builds6/6 PASS; runs6/6 exit0; complete-output comparisons6/6 PASS, with CRLF/LF normalization only. Logs and commands are retained in results.json. This verifies the supplied sample inputs, not every possible branch or input.

Existing image sha256:35d40304542c8689331f8cab17c65926cdf48fe711e289321d71924b230a7d29 (SDK10.0.401/runtime10.0.12); one task-owned container cstudy-semantic-task6-batch2-20261002, network none,2CPU/2GB, cleared package sources, sequential build/run, build timeout120s/run15s. Container removal exit0. Existing containers were untouched. No install, source repair, generated page, main, deployment, service, security or credential change.

verify.py is an executed harness, not a standalone repository CLI. Reproduce in a private directory with expectations.json, NuGet.Config containing cleared packageSources, and copies of these six originals under samples/lesson-NN. Use a unique container name and the existing image only. Fixture copies/build outputs are not committed.

Cumulative original coverage10/35 (prior07/12/14/15 plus this batch); remaining25 originals and191 existing Console examples. Additional62 Console and31HTTP checks are separate prior evidence. CS07 remains IN_PROGRESS; UI/device/platform acceptance remains outstanding.

Work push must contain [skip publish] to use the existing workflow guard and avoid publication. No workflow settings are changed.

Independent read-only reviewer `review_batch2` approved source/teaching expectations, baseline hashes and6/6 logged results; no rerun. Creation/copy exit0 assertions exist in runner but full lifecycle logs were not retained; cleanup exit0 and image inspect are preserved in lifecycle.json. SDK/runtime versions are prior measurements for the pinned image.
