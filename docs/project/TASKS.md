# Tasks — C# Learning Lab 5.1.0

Updated: 2026-10-02。古いCS02/CS03時点のcheckpointは`docs/archive/2026-10-01-stale-project-state/`に保存。現在の引継ぎは本書を正本とする。

|Task|Status|実績・残件|
|---|---|---|
|教材/UI5.1・静的公開|完了履歴|root TASKS / AI_WORK_STATEの2026-09実績を参照。今回再公開していない|
|CS07 C#実測検証|IN_PROGRESS|300/300ビルド、追加Console62/62出力一致、Web10例31HTTP検査成功。元教材35/35件の選定意味的検証PASS。既存Console159/193件PASS、残り34件。供給入力/選定HTTP検証で全分岐保証ではない|
|実オリジンUI E2E|TODO|HTTP/HTTPSナビゲーション、永続保存、サブパス、PC/Safari/iPhone/iPad|
|ブラウザー内C#ランナー|DEFERRED|配信サイズ・隔離・停止・メモリ制約の検討が必要。未搭載|
|CS11 Rules全文同期|DEFERRED|既存RULES_SOURCEの未同期事項を維持|

Evidence: `docs/validation/2026-10-01-dotnet/README.md`。コンパイル成功と実行出力照合は分けて扱う。

2026-10-02追加Evidence: `docs/validation/2026-10-02-semantics/README.md`。4/4選定例PASS（本バッチ100%）。CS07全体は未完了。入力ソース39e495cとremote baseline415a32aの対象コード/本文hash一致を確認。

2026-10-02 batch2: original03/04/05/06/08/09 complete-output6/6 PASS; cumulative10/35, remaining25 originals +191 existing Console examples. No source defects found for these inputs. Evidence: `docs/validation/2026-10-02-semantics-batch2/README.md`. CS07 remains IN_PROGRESS. Task container removed.

2026-10-02-semantics-batch3: 10/10 selected originals PASS; cumulative20/35, remaining15 originals +191 existing Console examples. Evidence: `docs/validation/2026-10-02-semantics-batch3/README.md`. CS07 IN_PROGRESS; task container removed.

2026-10-02-semantics-batch4: 8/8 selected originals PASS; cumulative28/35, remaining7 originals +191 existing Console examples. Evidence: `docs/validation/2026-10-02-semantics-batch4/README.md`. CS07 IN_PROGRESS; task container removed.

2026-10-02-semantics-batch5: cumulative originals33/35, existing Console0/191; remaining2 originals +191 existing Console. Evidence: `docs/validation/2026-10-02-semantics-batch5/README.md`. CS07 IN_PROGRESS; task container removed.

2026-10-02-semantics-batch6: cumulative originals35/35, existing Console0/191; remaining0 originals +191 existing Console. Evidence: `docs/validation/2026-10-02-semantics-batch6/README.md`. CS07 IN_PROGRESS; task container removed.

Inventory correction: expanded201 projects =8Web +193Console (191 ordinary csharp +1 csharp-input deep-04-03 +1 csharp-file deep-21-03). Earlier191 figures exclude these2 input/file examples; both remain in semantic scope. Current remaining193 Console total, not191.

2026-10-02-existing-console-early: existing Console47/193 PASS, remaining146; originals35/35 selected contracts covered. Evidence: `docs/validation/2026-10-02-existing-console-early/README.md`. CS07 IN_PROGRESS.

2026-10-02-existing-console-middle: existing Console123/193 PASS, remaining70; originals35/35 selected contracts covered. Evidence: `docs/validation/2026-10-02-existing-console-middle/README.md`. CS07 IN_PROGRESS.

2026-10-02-existing-console-late: existing Console159/193 PASS, remaining34; originals35/35 selected contracts covered. Evidence: `docs/validation/2026-10-02-existing-console-late/README.md`. CS07 IN_PROGRESS.
