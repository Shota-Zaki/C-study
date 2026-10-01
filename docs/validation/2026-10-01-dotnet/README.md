# .NET実測検証 — 2026-10-01

教材ソースSHA: `33308554299df79d59574469ba24defb2b904ad1`。この検証では教材コードを変更していない。`input-sha256.json`は.cs / .csproj / expected.txtの664ファイルを固定する。

## 結果

- 既存236件 + 追加64件 = 300プロジェクトの `dotnet build --nologo --disable-build-servers` がすべて成功。`builds.json`に全コマンドの終了コードと出力を保存。
- 追加Console例62件を実行し、終了コード0かつexpected.txtと全文一致（CRLF/LFのみ正規化）。`visual-outputs.json`。
- 追加Web例2件はGET正常・404とPOST正規化・空白拒否の5リクエスト成功。
- 既存Web例8件は26リクエスト成功。route型制約、query default/trim、入力100/101境界、Todo作成/取得/更新/削除、削除後404、DI、Optionsの初期値を確認。`existing-web.json`。

環境: .NET SDK10.0.401、runtime10.0.12、Ubuntu24.04/linux-arm64。イメージ: `mcr.microsoft.com/dotnet/sdk@sha256:35d40304542c8689331f8cab17c65926cdf48fe711e289321d71924b230a7d29`。

## 隔離・再現

Docker container `cstudy-sdk-20261001`をnetwork none、CPU4、memory4gで作成。samplesを専用一時コピーからdocker cpし、外部packageSourcesをclearしたNuGet.Configでビルドした。最初のbind mountはColimaで空に見え、MSB1009だったため、コピー存在確認後に全件やり直した。教材コードの失敗ではない。採用したログはコピー後の実測のみ。

同梱のPythonファイルは今回使った実行ハーネスの記録であり、汎用CLIではない。再実行時にはrepo/temp/containerのパスを実環境へ合わせる。build harnessは4並列、各build120秒。実行はtimeout15秒、Webはtimeout25秒とcurl max-time3秒。Webはコンテナー内loopbackのみでホスト公開なし。HTTPのbodyとstatusを個別照合し、実行サーバーを各検査後に終了。終了時に専用コンテナーも削除した。

## 未完了

既存Console例191件および元教材35プロジェクト等の意味的な出力照合・入力/ファイル操作の個別確認は残る。全300件が実行検証済みという意味ではない。意図的エラーや部分例はprojectがないためbuild件数に含めない。production公開、実オリジンでの教材UI E2E、Safari/iPhone/iPad実機、ブラウザー内C#ランナーは本検査の対象外。

生成manifestのUNVERIFIEDは生成時の初期値である。今回の固定ソースに対する実測結果は本ディレクトリを参照し、将来の変更へ無条件に転用しない。
