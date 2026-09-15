# NEXT_WORK

対象: `Shota-Zaki/C-study` / Version 5.0.0。
`work` を開発・検証の正本、`main` を公開物の正本として再開してください。GitHub Pagesへのデプロイは成功済みです。

## 次のWork Unit

.NET SDKが利用可能な環境で、既存236プロジェクトと追加64プロジェクトをビルドし、Consoleサンプルの想定出力とWebサンプルの応答を実測で照合します。現時点の想定出力を実測値として扱わないでください。

続いて実HTTP/HTTPSでPCとSafariの操作、永続保存、サブパス配置を検査します。

## 任意機能の保留

ブラウザー内C#実行は未搭載です。無料の静的配信は可能な構成があるため、有料前提に変えず、WebAssemblyとC#コンパイラーの実配信サイズ・隔離・停止・メモリ制約を検証してから実装判断してください。制約と受入条件は docs/HOSTING_AND_RUNNER.md にあります。

## 維持する決定

左側はChapter → Lesson → ページ内見出し、右側は用語欄、現在Chapterは初期状態で開きます。案内セクションとスローガンは再導入せず、既存96演習・160問・保存IDを維持してください。

生成入口は scripts/build_visual.py。追加コンテンツの正本は content/visual/lessons.json です。
