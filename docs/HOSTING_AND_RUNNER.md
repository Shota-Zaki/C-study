# 無料公開とC#実行の検討

確認日: 2026-09-15

## 今回の配布方式

公開用は静的HTML・CSS・JavaScript・SVG・ダウンロード用サンプルです。Functions、データベース、外部実行API、課金APIは使いません。教材の生成済みファイルを配信するだけの構成です。

公開用ファイル数・展開後サイズ・最大ファイルは `validation/visual/release-manifest.json` に記録しています。無料枠の公開容量条件に収まることと、将来のアクセス数・ビルド頻度が常に制限内であることは別です。

| サービス | 公式条件 |
|---|---|
| Cloudflare Pages Free | サイト最大20,000ファイル、1ファイル最大25 MiB。Git連携のビルドは月500回 |
| GitHub Pages / GitHub Free | 公開リポジトリが対象。公開サイト最大1GB。月間帯域100GBはソフト上限 |

CloudflareのDirect Uploadではアップロード手段による上限も確認してください。今回の公開用ファイルは、1,000件未満の構成にしています。

## ブラウザー内のC#実行

.NETのWebAssembly実行基盤とコンパイラーをブラウザーへ配信する構成であれば、有料のC#実行サーバーを必須にはしません。MicrosoftはスタンドアロンBlazor WebAssemblyの静的ホスティングを説明しています。ただし、配信できることと、ユーザー入力コードのコンパイル・隔離・停止を安全に実装できたことは別です。

今回の作業環境には.NET SDKがなく、外部配布先からの取得もできなかったため、ランナーの取得・ビルド・動作検証を完了できませんでした。そのためランナーは同梱していません。無料枠では不可能という判断ではありません。WebAssemblyは次回候補であり、具体的な配布バンドルの容量・モバイル性能を検証した結果ではありません。

## 実装する場合の受入条件

実C#のコンパイルとConsole出力、コンパイルエラーの行番号、実行時例外、再実行時の状態破棄、入力の扱い、無限ループを止める仕組み、実行時間制限、ファイルとネットワークの制約を検証します。JavaScriptによる簡易的な読み替えや固定出力の表示は代替にしません。

任意のコードはホストページと分離し、通信・ストレージ・DOMへの影響を確認します。Web APIのサーバー起動、OS依存処理、NuGet追加などを、単純なConsoleサンプルと同じ対応範囲として扱わないでください。

## 公式資料

- Cloudflare Pages limits: https://developers.cloudflare.com/pages/platform/limits/
- GitHub Pages limits: https://docs.github.com/en/pages/getting-started-with-github-pages/github-pages-limits
- Microsoft / Blazor WebAssembly deployment: https://learn.microsoft.com/en-us/aspnet/core/blazor/host-and-deploy/webassembly/?view=aspnetcore-10.0

料金・制限・提供条件は変更されるため、公開時は公式ページを再確認してください。
