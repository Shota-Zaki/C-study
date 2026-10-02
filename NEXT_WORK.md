# NEXT_WORK

対象: `Shota-Zaki/C-study` / Version 5.1.0。
`work` を開発・検証の正本、`main` を公開物の正本として再開してください。本文途中の図解追加・単元別の説明順への再構成、GitHub Actionsのビルド/監査、`main` 公開、GitHub Pagesデプロイまで完了しています。

## 次のWork Unit

2026-10-01に300プロジェクトの実ビルド、追加Console62件の出力一致、Web10例31HTTP検査が成功しました。証拠は `docs/validation/2026-10-01-dotnet/README.md`。2026-10-02に元教材07/12/14/15の4例も意味的出力照合に成功しました。次は残り31元教材プロジェクト・191既存Console例の出力照合です。証拠は `docs/validation/2026-10-02-semantics/README.md`。最新正本は `docs/project/NEXT_WORK.md`。

続いて実HTTP/HTTPSでPCとSafariの操作、永続保存、サブパス配置を検査します。実機確認ではiPhone/iPadの狭幅表示、横スクロール表、本文途中の図解、Chapter内目次の操作を重点確認します。

## 教材構成の維持

全レッスンを同じテンプレート順に戻さないでください。単元ごとの理解対象に合わせ、必要な位置へ図解を挟む構成を維持します。条件分岐・配列/反復・値型/参照型・LINQ・非同期・HTTP/Web APIなどは、それぞれ異なる説明順と図の形式を使います。

新規教材を追加・変更するときは `content/pedagogy/lessons.json` と `content/pedagogy/supplements.json`、`scripts/pedagogy.py`、`assets/css/pedagogy.css` を確認し、文章→コード→図→確認という固定テンプレートへ機械的に統一しないでください。

## 任意機能の保留

ブラウザー内C#実行は未搭載です。無料の静的配信は可能な構成があるため、有料前提に変えず、WebAssemblyとC#コンパイラーの実配信サイズ・隔離・停止・メモリ制約を検証してから実装判断してください。制約と受入条件は `docs/HOSTING_AND_RUNNER.md` にあります。

## 維持する決定

左側はChapter → Lesson → ページ内見出し、右側は用語欄、現在Chapterは初期状態で開きます。案内セクションとスローガンは再導入せず、既存96演習・160問・保存IDを維持してください。

生成入口は `scripts/build_visual.py`。追加コンテンツの正本は `content/visual/lessons.json` と `content/pedagogy/` 配下です。
