# Original lesson semantic output — 2026-10-02

Run input: `39e495c3108e46459a74606029a559a9302b84e5`. Compatible latest remote baseline: `415a32a8e7cce5a37e6b351c95c46cd79c54f2e1` (2026-10-01 manifest regeneration). All four Program.cs/Lesson.csproj and corresponding rendered lesson HTML hashes match at both commits; expectations.json fixes them.

Four original lesson projects pass actual sequential .NET builds and full expected-output matching (CRLF/LF normalization only):

| Lesson | Expected output | Meaning checked |
| --- | --- | --- |
| 07 | 6 / 8 / 2 | default step1, named step3, ref increments caller variable |
| 12 | 学習完了 | injected ConsoleSender receives Complete through IMessageSender |
| 14 | True / False / 80 → 95 | record value equality, distinct references, with leaves original score unchanged |
| 15 | 80 / 2 / 10 | dictionary lookup success, HashSet removes duplicate, generic First returns first int |

Expected values were established from code and each lesson's 想定出力/処理順 before running. results.json retains each command, build output, exit code, observed output and semanticMatch. Four builds and four runs all exit0, all four semanticMatch=true.

Existing SDK image `sha256:35d40304542c8689331f8cab17c65926cdf48fe711e289321d71924b230a7d29`, SDK10.0.401/runtime10.0.12. Task-only copied samples in container cstudy-semantic-task3-20261002; network none,2CPU,2GB, packageSources clear, sequential builds120sec/run15sec. Container removed successfully. No existing service restart, software install, source/generated lesson change, main merge or publication.

verify.py records the executed harness, not a self-contained repository CLI. To reproduce, create a dedicated directory containing expectations.json, NuGet.Config with packageSources clear, and copies of the four original samples under samples/lesson-07,12,14,15; use a unique task-owned container name and the same existing image, then run the harness. Do not run against existing containers or source-tree build directories.

CS07 remains IN_PROGRESS. Original lesson/project outputs:4 of35 semantically checked in this batch; remaining31 plus existing expanded Console191 require source/lesson review. Prior additional Console62 and HTTP31 assertions remain separate evidence. UI real-origin and Safari/device QA, browser runner and full rules sync remain unfinished/deferred.
