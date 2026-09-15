# 保守・再生成

## 正本

| 変更対象 | 編集するファイル |
|---|---|
| 32図解の値・文言、64実例、重要点 | `content/visual/lessons.json` |
| 既存文章の置換 | `content/visual/copy-edits.json` |
| 図のレイアウト、実例のHTML | `scripts/visual_components.py` |
| 既存詳細解説の本文 | `content/deep/*.md` |
| 補助教材 | `content/guides/*.md` |
| 用語定義 | `content/glossary-expanded.json` |
| 元教材テンプレート | `content/templates/` |
| 最終レイアウト・目次・用語配置 | `scripts/build_visual.py` |
| スタイル | `assets/css/visual.css` |
| 目次・用語リンク・モバイルナビ | `assets/js/expanded.js` |
| 用語欄の開閉、.cs保存 | `assets/js/visual.js` |
| 既存の保存・確認問題・検索 | `assets/js/site.js` |

HTMLと `samples/visual/` は生成物です。直接編集すると再生成で上書きされます。

## 再生成と検査

```sh
python -m pip install -r scripts/requirements.txt
python scripts/build_visual.py
python scripts/audit_visual.py
node --check assets/js/site.js
node --check assets/js/expanded.js
node --check assets/js/visual.js
```

DOM表示検査は `python scripts/test_visual_browser.py` です。PlaywrightとChromiumが必要です。`CSTUDY_CHROMIUM` にブラウザーの実行ファイルを指定できます。未指定時はPATH上のChromium、次にPlaywright標準のChromiumを使用します。このテストはHTML・CSS・JavaScriptをインメモリで読み込み、保存領域を代替する検査であり、公開URLに対するE2Eではありません。

追加64プロジェクトのコンパイル確認は次のコマンドです。SDK自体はダウンロードしません。SDK不足は終了コード2、失敗は1、全ビルド成功は0です。ビルド成功は出力内容やAPI仕様の検証を意味しません。

```sh
python scripts/verify_visual_samples.py --build
```

既存236プロジェクトは `python scripts/verify_dotnet.py --build` で別途確認します。

`bash scripts/run_release_audits.sh --browser` は、再生成、静的検査、DOM検査、既存・追加サンプルのビルド確認を実行します。ブラウザー検査を省く場合は `--browser` を外します。.NET未確認を成功扱いにせず終了コード2を返します。

## 公開用の書き出し

```sh
python scripts/package_public.py --output ../C-study_public
```

出力先にはHTML、assets、本文から参照されるファイルと `.nojekyll`、robots.txtだけを書き出します。既存ディレクトリは、誤消去を避けるため空の場合に限って利用します。生成後の公開用ディレクトリをホスティングサービスに配置してください。

## 変更時の注意

演習の `data-draft`、レッスンID、確認問題の正解値、保存キー `cstudy.learning.v2` は既存の保存データと関係します。見た目の変更だけで値を変えないでください。用語の移動時は元のIDを維持し、本文内リンクの参照先を失わないようにしてください。

C#実行機能を追加する場合は、実コンパイル、構文エラー、標準出力、実行の停止、無限ループ、タイムアウト、Console入力、再実行時の状態破棄、サブパス配置、モバイルのメモリ使用量を先に確認します。固定出力の表示やJavaScriptの独自解釈をC#実行として扱いません。
