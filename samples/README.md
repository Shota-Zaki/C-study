# C#サンプルの使い方

## 分類

`manifest.json` は275件を管理しています。入力版の独立プロジェクト35件と、追加教材から取り出した240件です。追加240件の内訳は、独立例201件、意図的な失敗例32件、部分例5件、テスト用の例2件です。独立したプロジェクトは合計236件あります。

`Program.cs` と `Example.csproj` を持つ追加例は、同じ例同士を連結せず、そのフォルダー単位でビルドします。`.cs.txt` は参照用のコードです。意図的な失敗例や必要な周辺コードのない部分例を、一括起動へ混ぜません。

マニフェストは各例の元Markdown、対応するHTML、種類、コードの場所、プロジェクトの場所を記録しています。**すべて実ビルド・実行は未検証**です。コードを読んで説明した想定結果と、実測を区別してください。

## 最小の確認

```powershell
dotnet build samples/expanded/deep/01/example-01/Example.csproj
dotnet run --project samples/expanded/deep/01/example-01/Example.csproj
```

この例の想定出力は「学習開始」「30」「30」の3行です。`minutes`を50にしても、既に計算した`total`は30のままという状態変化を確認します。

## 統合Web API

```powershell
dotnet build samples/expanded/deep/32/example-01/Example.csproj
dotnet run --project samples/expanded/deep/32/example-01/Example.csproj --no-launch-profile -- --urls http://127.0.0.1:5080
```

起動した端末をそのままにして、別の端末から `deep-dives/32.html` のHTTP確認手順を実施します。終了は起動端末でCtrl+Cです。学習用のメモリ保存であり、再起動するとデータは消えます。認証・認可・永続保存・本番公開の設計は別に必要です。

## 保守用の一括ビルド

```powershell
python scripts/verify_dotnet.py --build
python scripts/verify_dotnet.py --run-id deep-01-01
```

前者は236件の独立プロジェクトをビルドしますが、自動起動しません。後者は指定したコンソール例だけをビルド後に起動し、15秒でタイムアウトします。対象コードを先に読みます。Web・ファイル・入力待ち・失敗例はこの一括起動の対象になりません。

結果は `docs/validation/dotnet.json` に記録します。SDKが見つからないときは終了コード2、状態UNVERIFIEDです。ビルド成功だけで出力や業務要件の正しさをPASSにしません。

元教材の演習解答や説明内の部分例にはHTML / `content/course.json`だけに含まれるものもあります。すべての表示断片が独立プロジェクトになっているわけではありません。必要な周辺設定を本文で確認します。
