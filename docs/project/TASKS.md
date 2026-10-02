# Tasks — C# Learning Lab 5.1.0

Updated: 2026-10-02。古いCS02/CS03時点のcheckpointは`docs/archive/2026-10-01-stale-project-state/`に保存。現在の引継ぎは本書を正本とする。

|Task|Status|実績・残件|
|---|---|---|
|教材/UI5.1・静的公開|完了履歴|root TASKS / AI_WORK_STATEの2026-09実績を参照。今回再公開していない|
|CS07 C#実測検証|IN_PROGRESS|300/300ビルド、追加Console62/62出力一致、Web10例31HTTP検査成功。元教材4件（07/12/14/15）の意味的出力照合PASS。元教材残り31件・既存Console191件の出力照合は残る|
|実オリジンUI E2E|TODO|HTTP/HTTPSナビゲーション、永続保存、サブパス、PC/Safari/iPhone/iPad|
|ブラウザー内C#ランナー|DEFERRED|配信サイズ・隔離・停止・メモリ制約の検討が必要。未搭載|
|CS11 Rules全文同期|DEFERRED|既存RULES_SOURCEの未同期事項を維持|

Evidence: `docs/validation/2026-10-01-dotnet/README.md`。コンパイル成功と実行出力照合は分けて扱う。

2026-10-02追加Evidence: `docs/validation/2026-10-02-semantics/README.md`。4/4選定例PASS（本バッチ100%）。CS07全体は未完了。入力ソース39e495cとremote baseline415a32aの対象コード/本文hash一致を確認。
