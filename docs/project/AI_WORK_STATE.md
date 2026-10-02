# AI work state

Updated: 2026-10-02 / Asia-Tokyo
Repository: Shota-Zaki/C-study
Development: work / Publication: main
Current: CS07 IN_PROGRESS
Rules provenance: docs/rules/RULES_SOURCE.md (2.0.0; full snapshot remains deferred)

教材5.1の公開完了履歴はroot AI_WORK_STATEに維持。今回の実測ソースは33308554299df79d59574469ba24defb2b904ad1。

- 300/300 C# projects build successfully under SDK10.0.401/runtime10.0.12.
- 62/62 additional console examples match expected.txt exactly after newline normalization.
- 10 web examples pass31 HTTP assertions.
- Existing console/original-project semantic validation remains incomplete.
- Evidence: docs/validation/2026-10-01-dotnet/README.md.
- Dedicated network-isolated Docker container stopped/removed; no deployment or main change.

Resume: AGENTS → RULES_SOURCE → docs/project/TASKS → NEXT_WORK → evidence. 古い2026-09-14 checkpointはdocs/archive/2026-10-01-stale-project-stateへ保存済み。

- 2026-10-02: original lesson07/12/14/15 semantic outputs4/4 PASS. Input hashes compatible with remote415a32a; evidence docs/validation/2026-10-02-semantics/. Remaining31 original projects +191 existing Console examples. Dedicated container removed.

2026-10-02 batch2: original03/04/05/06/08/09 complete-output6/6 PASS; cumulative10/35, remaining25 originals +191 existing Console examples. No source defects found for these inputs. Evidence: `docs/validation/2026-10-02-semantics-batch2/README.md`. CS07 remains IN_PROGRESS. Task container removed.

2026-10-02-semantics-batch3: 10/10 selected originals PASS; cumulative20/35, remaining15 originals +191 existing Console examples. Evidence: `docs/validation/2026-10-02-semantics-batch3/README.md`. CS07 IN_PROGRESS; task container removed.

2026-10-02-semantics-batch4: 8/8 selected originals PASS; cumulative28/35, remaining7 originals +191 existing Console examples. Evidence: `docs/validation/2026-10-02-semantics-batch4/README.md`. CS07 IN_PROGRESS; task container removed.

2026-10-02-semantics-batch5: cumulative originals33/35, existing Console0/191; remaining2 originals +191 existing Console. Evidence: `docs/validation/2026-10-02-semantics-batch5/README.md`. CS07 IN_PROGRESS; task container removed.

2026-10-02-semantics-batch6: cumulative originals35/35, existing Console0/191; remaining0 originals +191 existing Console. Evidence: `docs/validation/2026-10-02-semantics-batch6/README.md`. CS07 IN_PROGRESS; task container removed.

Inventory correction: expanded201 projects =8Web +193Console (191 ordinary csharp +1 csharp-input deep-04-03 +1 csharp-file deep-21-03). Earlier191 figures exclude these2 input/file examples; both remain in semantic scope. Current remaining193 Console total, not191.

2026-10-02-existing-console-early: existing Console47/193 PASS, remaining146; originals35/35 selected contracts covered. Evidence: `docs/validation/2026-10-02-existing-console-early/README.md`. CS07 IN_PROGRESS.

2026-10-02-existing-console-middle: existing Console123/193 PASS, remaining70; originals35/35 selected contracts covered. Evidence: `docs/validation/2026-10-02-existing-console-middle/README.md`. CS07 IN_PROGRESS.

2026-10-02-existing-console-late: existing Console159/193 PASS, remaining34; originals35/35 selected contracts covered. Evidence: `docs/validation/2026-10-02-existing-console-late/README.md`. CS07 IN_PROGRESS.

2026-10-02-existing-console-guides: existing Console193/193 PASS, remaining0; originals35/35 selected contracts covered. Evidence: `docs/validation/2026-10-02-existing-console-guides/README.md`. CS07 IN_PROGRESS.

Current handoff: assigned source-output verification COMPLETE (original35/35 selected scenarios; expanded Console193/193 includingstdin/file). Full ledger `docs/validation/2026-10-02-existing-console-coverage/README.md`; no source defect/fix. CS07 overall stays IN_PROGRESS. Next acceptance is real-origin UI navigation/storage/subpath and Safari/device checks; browser runner and rules sync remain separate deferred gates. No main/deployment.

2026-10-02 local-origin UI checkpoint:10 manually observed criteria PASS on task-owned HTTP /course/ (native navigation/reload and origin persistence, no storage substitute). Evidence `docs/validation/2026-10-02-local-origin-ui/README.md`. Browser chooser control stalled; export capture/further UI/published HTTPS/native Safari/device scopes remain unverified/blocked. Task-only server40552 stopped, no shared services. CS07 IN_PROGRESS; source-output scope remains complete.

2026-10-02 local import/storage: 10/10 bounded checks PASS (8 actual loopback HTTP UI, 2 actual UI with injected Storage.setItem quota fault). Five invalid imports retain exact stored bytes; valid import reload/restoration and captured Blob export checked. No source fixes. Evidence: `docs/validation/2026-10-02-import-storage/README.md`. CS07 IN_PROGRESS; published HTTPS/native Safari/iPhone/iPad and remaining responsive/keyboard criteria remain unverified. Task-owned browser/server stopped.
