# VALIDATION結果

監査日: 2026-09-14

## 結論

静的構造、ブラウザーUI、学習データ、リンク、アクセシビリティ、C#コードのレキシカル健全性はすべて監査PASS。C#の実コンパイル・実行だけは、成果物作成環境に `dotnet` SDKが存在しないため **未検証** としている。未検証項目をPASSには数えていない。

## 監査サマリー

| 監査 | 結果 |
|---|---:|
| 静的サイト・教材構造 | 830 / 830 PASS |
| Headless Chromium UI/機能 | 553 / 553 PASS |
| アクセシビリティ静的監査 | 3,687 / 3,687 PASS |
| C#レキシカル健全性 | 262スニペット、0 FAIL |
| 内部リンク | 1,515件、0 FAIL |
| ローカルHTTPスモーク | 45リソース 200、欠損パス 404 |
| ページ内/リンク先フラグメント | 572件、0 FAIL |
| 外部URL構造 | 61ユニークURL、0 FAIL |
| 外部URL実アクセス | 61ユニークURLを2026-09-14にWeb取得で確認 |
| C#実ビルド / 実行 | 未検証（SDKなし） |

機械可読の詳細は `docs/browser_audit.json`、`docs/a11y_audit.json`、`docs/link_audit.json`、`docs/http_smoke.json`、`docs/csharp_static_audit.json` に保存している。

## 静的監査

`scripts/validate_static.py` で以下を確認した。

- 8章、32レッスン、各章4レッスン
- Lesson 01〜32の連番と章所属
- 160問、640選択肢、640個別解説
- 回答インデックスの範囲
- 96演習、3制作課題
- 単独教材用説明、worked flow、不具合修正例の存在
- 旧比較教材の語・構文・意味パターン残留
- JavaScript を必要語として維持
- index / 404 / settings / 32 lessons / 3 project pages / robots.txt
- title / description / viewport / canonical / lang / skip link / nav landmark
- 内部リンクの存在
- Lesson 01〜32の前後移動とLesson 32→制作課題の導線
- ページ内目次
- 各レッスン5問 / 20個別解説 / 3下書き欄
- コード領域の言語ヘッダーとCopy操作
- 404の `noindex`
- desktop 3カラム、tablet TOC縮退、mobile drawer、dark theme、reduced motion、visible focusのCSS条件
- localStorage名前空間とJSON import防御実装
- Lesson 16 / 21 / 28の固定回帰条件

## ブラウザー監査

`scripts/browser_audit.py` は実際のHeadless Chromiumレンダリングエンジンで生成HTML・CSS・JavaScriptを読み込み、553項目を検査した。

監査環境ではlocalhostおよび `file://` へのページ遷移がポリシーで遮断されるため、各生成HTMLを `set_content` で読み込み、生成済みCSS/JavaScriptを同一ページへ注入して検証した。opaque originではネイティブlocalStorageが利用できないため、監査ハーネス内だけでlocalStorageを同等APIのメモリ実装へ置換している。サイト本体の保存先は通常の `localStorage` のままである。

主な確認内容:

- 全32レッスンのDesktop描画
- H1、問題数、選択肢解説数、下書き欄数
- ページ全体の横スクロールなし
- Desktopの左ナビ + 本文 + 右TOC
- Tablet代表ページで本文優先 + 右TOC非表示 + 折りたたみ目次表示
- Mobile代表ページでdrawer初期退避、ARIA状態、Escape/ボタン開閉、本文1カラム、折りたたみ目次、横スクロールなし
- 検索でLINQ教材を取得
- 完了状態、復習マーク、下書き、確認問題採点
- Light / Darkテーマ
- 壊れた既存保存データから安全に初期状態へ復帰
- JSON exportのファイル名・内容
- JSON importの正常系
- JSON構文不正、存在しないレッスンID、不正な下書き型、512 KiB超過を拒否
- import失敗時に既存データを維持
- skip link、キーボードフォーカス、ボタン名のスモークテスト

## JSON importの破壊防止

`assets/js/site.js` はインポート時に次を検証し、すべて成功した場合だけ状態を置き換える。

- ファイルサイズ: 512 KiB以下
- 最上位: object
- version: 2
- theme: light / dark / system
- completed / review: 正しいレッスンID、重複なし
- lastLesson: null または正しいレッスンID
- quiz: レッスンID、回答配列、回答値0〜3、score範囲
- drafts: 既知の演習キー、文字列型、1件100,000文字以下、合計400,000文字以下

## アクセシビリティ

`scripts/a11y_audit.py` で全HTMLのmain見出し階層、操作要素のアクセシブルネーム、dialog名、フォームコントロールのラベルを検査した。CSSではfocus-visible、reduced motion、dark themeを確認した。

代表的なコントラスト比:

- Light本文 / 背景: 16.29:1
- Light補助文字 / 背景: 5.09:1
- Lightアクセント / 背景: 6.29:1
- Dark本文 / 背景: 15.01:1
- Dark補助文字 / 背景: 7.25:1
- Darkアクセント / 背景: 8.90:1

通常文字は4.5:1以上、フォーカス指標は3:1以上を監査基準にした。

## リンク

`scripts/link_audit.py` でローカルリンク1,515件、フラグメント572件、外部URL61件の構造を検査した。ローカルの欠損先・欠損アンカーは0件。

外部61URLは2026-09-14にWeb取得でも確認し、ページ本文または正規のリダイレクト先へ到達した。Microsoft Learn側のコンソール作成チュートリアルは現行導線を反映した。

## ローカルHTTPスモーク

`scripts/http_smoke.py` で生成サイトをローカルHTTPサーバーへ載せ、HTMLから参照されるローカルリソース45件がHTTP 200になることを確認した。存在しないテストパスはHTTP 404になり、`404.html` 自体も200で取得できる。静的ホスティングでカスタム404を使うかどうかはホスティング側の404規約に依存する。

## SEO

- 全HTMLにtitle、description、viewport、canonical、OGP、favicon
- `lang="ja"`
- `404.html` は `noindex,follow`
- `robots.txt` を同梱
- 公開URL未確定のためcanonicalは相対URL
- sitemapは `scripts/generate_sitemap.py <公開ベースURL>` で生成可能

## C#コード監査

`scripts/audit_csharp_code.py` は次の262スニペット/ファイルをレキシカル検査した。

- 各Lessonのメイン例
- worked flow
- 修正後コード
- C#重点コード
- 基礎演習解答
- 標準/応用演習解答
- 制作課題コード
- `samples/` 配下の35個の `Program.cs`

通常文字列への実改行、未終端文字列、未終端コメント、`()[]{}` の不整合は0件。これはコンパイラではないため、構文・型・API互換性の最終保証には使用しない。

## C#実ビルド / 実行 — 未検証

成果物作成環境には `dotnet`、`csc`、`mono` がなく、外部バイナリの取得も実行環境から行えなかった。そのため `dotnet build` / `dotnet run` は実施できていない。

`./scripts/build_samples.sh` の実行結果:

```text
UNVERIFIED: dotnet SDK is not installed in this environment.
exit_code=2
```

SDKがある環境では `scripts/build_samples.sh` が `samples/` 配下の全35 `.csproj` を列挙して `dotnet build` を実行する。対象は .NET 10 / C# 14。2026-09-14時点の.NET公式ダウンロードページではSDK 10.0.401、C# 14.0が掲載されている。

## 再検証

```bash
python scripts/validate_static.py
python scripts/link_audit.py
python scripts/http_smoke.py
python scripts/a11y_audit.py
python scripts/audit_csharp_code.py
python scripts/browser_audit.py
./scripts/build_samples.sh
```

まとめて行う場合:

```bash
./scripts/run_all_audits.sh
```
