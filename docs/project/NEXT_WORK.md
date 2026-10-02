# Next work

Updated: 2026-10-02。Current: CS07（C#実測検証）。

1. `docs/validation/2026-10-01-dotnet/README.md`で固定ソースと実測範囲を確認。
2. 既存Console例191件と元教材残り15プロジェクトについて、対応本文と既存証拠を読み、意味的期待値を用意して照合。受入済みバッチを新規実績として再実行しない。入力・ファイル操作例は専用一時領域。意図的エラー・部分例を正常実行扱いしない。
3. 教材UIの実HTTP/HTTPS・永続保存・サブパスを検査。Safari/iPhone/iPad実機は利用可能な環境で確認。

300プロジェクトのビルド、追加Console62件の全文出力照合、Web10例31リクエストは完了済み。SDK10.0.401の既存Docker imageを利用可能。専用検証コンテナーは終了済み。教材コード・生成物・main・公開環境は今回変更していない。

単元ごとの説明順・本文図解、32レッスン・96演習・160問・保存IDを維持。生成入口はscripts/build_visual.py。任意のブラウザー内ランナーを暗黙に追加しない。

追加証拠: `docs/validation/2026-10-02-semantics/README.md`。4例は専用network-noneコンテナーで順次実行、終了後削除済み。

2026-10-02 batch2: original03/04/05/06/08/09 complete-output6/6 PASS; cumulative10/35, remaining25 originals +191 existing Console examples. No source defects found for these inputs. Evidence: `docs/validation/2026-10-02-semantics-batch2/README.md`. CS07 remains IN_PROGRESS. Task container removed.

2026-10-02-semantics-batch3: 10/10 selected originals PASS; cumulative20/35, remaining15 originals +191 existing Console examples. Evidence: `docs/validation/2026-10-02-semantics-batch3/README.md`. CS07 IN_PROGRESS; task container removed.
