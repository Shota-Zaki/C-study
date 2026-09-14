# 技術説明の一次情報

対象：.NET 10 / C# 14。確認日：2026年9月14日。Microsoft公式資料を基本とし、HTTPの意味はIETFのRFCを補助的に使用。

## 説明の基準

値型・参照型を物理配置だけで説明せず、値と参照のコピーから説明する。nullable参照型は静的な注釈・解析と実行時検証を分ける。Taskはスレッド自体と同一視しない。LINQのクエリ作成・列挙・結果確定の時点を分ける。GCとDisposeを分け、DIの寿命と状態の安全性を分ける。

## 資料一覧

| ID | 一次情報 | URL |
|---|---|---|
| sdk | .NET 10 SDKのダウンロード | https://dotnet.microsoft.com/ja-jp/download/dotnet/10.0 |
| intro | .NETの概要 | https://learn.microsoft.com/ja-jp/dotnet/core/introduction |
| support | .NETのサポートポリシー | https://dotnet.microsoft.com/ja-jp/platform/support/policy |
| install | コンソールアプリの作成 | https://learn.microsoft.com/ja-jp/dotnet/core/tutorials/with-visual-studio-code |
| top | トップレベルステートメント | https://learn.microsoft.com/ja-jp/dotnet/csharp/fundamentals/program-structure/top-level-statements |
| types | C#の型システム | https://learn.microsoft.com/ja-jp/dotnet/csharp/fundamentals/types/ |
| var | 暗黙的に型指定されるローカル変数 | https://learn.microsoft.com/ja-jp/dotnet/csharp/programming-guide/classes-and-structs/implicitly-typed-local-variables |
| readonly | readonlyキーワード | https://learn.microsoft.com/ja-jp/dotnet/csharp/language-reference/keywords/readonly |
| string | 文字列補間 | https://learn.microsoft.com/ja-jp/dotnet/csharp/language-reference/tokens/interpolated |
| parse | 数値文字列の解析 | https://learn.microsoft.com/ja-jp/dotnet/standard/base-types/parsing-numeric |
| numeric | 組み込みの数値変換 | https://learn.microsoft.com/ja-jp/dotnet/csharp/language-reference/builtin-types/numeric-conversions |
| selection | ifとswitch | https://learn.microsoft.com/ja-jp/dotnet/csharp/language-reference/statements/selection-statements |
| pattern | パターンマッチング | https://learn.microsoft.com/ja-jp/dotnet/csharp/fundamentals/functional/pattern-matching |
| loop | 繰り返し文 | https://learn.microsoft.com/ja-jp/dotnet/csharp/language-reference/statements/iteration-statements |
| array | 配列 | https://learn.microsoft.com/ja-jp/dotnet/csharp/language-reference/builtin-types/arrays |
| method | メソッド | https://learn.microsoft.com/ja-jp/dotnet/csharp/programming-guide/classes-and-structs/methods |
| params | メソッドのパラメーター | https://learn.microsoft.com/ja-jp/dotnet/csharp/language-reference/keywords/method-parameters |
| nullable | null許容参照型 | https://learn.microsoft.com/ja-jp/dotnet/csharp/fundamentals/null-safety/nullable-reference-types |
| nullable-value | null許容値型 | https://learn.microsoft.com/ja-jp/dotnet/csharp/language-reference/builtin-types/nullable-value-types |
| class | クラス | https://learn.microsoft.com/ja-jp/dotnet/csharp/fundamentals/types/classes |
| ctor | コンストラクター | https://learn.microsoft.com/ja-jp/dotnet/csharp/programming-guide/classes-and-structs/constructors |
| property | プロパティ | https://learn.microsoft.com/ja-jp/dotnet/csharp/programming-guide/classes-and-structs/properties |
| required | required修飾子 | https://learn.microsoft.com/ja-jp/dotnet/csharp/language-reference/keywords/required |
| inherit | 継承 | https://learn.microsoft.com/ja-jp/dotnet/csharp/fundamentals/object-oriented/inheritance |
| override | override修飾子 | https://learn.microsoft.com/ja-jp/dotnet/csharp/language-reference/keywords/override |
| interface | インターフェイス | https://learn.microsoft.com/ja-jp/dotnet/csharp/language-reference/keywords/interface |
| value | 値型 | https://learn.microsoft.com/ja-jp/dotnet/csharp/language-reference/builtin-types/value-types |
| record | レコード | https://learn.microsoft.com/ja-jp/dotnet/csharp/language-reference/builtin-types/record |
| equality | 等値演算子 | https://learn.microsoft.com/ja-jp/dotnet/csharp/language-reference/operators/equality-operators |
| collection | コレクション | https://learn.microsoft.com/ja-jp/dotnet/csharp/language-reference/builtin-types/collections |
| generic | ジェネリック | https://learn.microsoft.com/ja-jp/dotnet/csharp/fundamentals/types/generics |
| exception | 例外処理 | https://learn.microsoft.com/ja-jp/dotnet/csharp/fundamentals/exceptions/ |
| using | usingステートメント | https://learn.microsoft.com/ja-jp/dotnet/csharp/language-reference/statements/using |
| lambda | ラムダ式 | https://learn.microsoft.com/ja-jp/dotnet/csharp/language-reference/operators/lambda-expressions |
| event | イベント | https://learn.microsoft.com/ja-jp/dotnet/csharp/programming-guide/events/ |
| linq | LINQクエリの概要 | https://learn.microsoft.com/ja-jp/dotnet/csharp/linq/get-started/introduction-to-linq-queries |
| linq-write | LINQクエリの記述 | https://learn.microsoft.com/ja-jp/dotnet/csharp/linq/get-started/write-linq-queries |
| enum | 列挙型 | https://learn.microsoft.com/ja-jp/dotnet/csharp/language-reference/builtin-types/enum |
| tuple | タプル型 | https://learn.microsoft.com/ja-jp/dotnet/csharp/language-reference/builtin-types/value-tuples |
| extension | 拡張メンバー | https://learn.microsoft.com/ja-jp/dotnet/csharp/programming-guide/classes-and-structs/extension-methods |
| io | ファイルとストリームI/O | https://learn.microsoft.com/ja-jp/dotnet/standard/io/ |
| json | System.Text.Jsonによるシリアル化 | https://learn.microsoft.com/ja-jp/dotnet/standard/serialization/system-text-json/how-to |
| date | 日付と時刻の型を選ぶ | https://learn.microsoft.com/ja-jp/dotnet/standard/datetime/choosing-between-datetime |
| culture | 数値文字列の書式 | https://learn.microsoft.com/ja-jp/dotnet/standard/base-types/standard-numeric-format-strings |
| async | 非同期プログラミング | https://learn.microsoft.com/ja-jp/dotnet/csharp/asynchronous-programming/ |
| cancel | マネージドスレッドのキャンセル | https://learn.microsoft.com/ja-jp/dotnet/standard/threading/cancellation-in-managed-threads |
| whenall | Task.WhenAll | https://learn.microsoft.com/ja-jp/dotnet/api/system.threading.tasks.task.whenall?view=net-10.0 |
| project | .NET SDKのプロジェクト設定 | https://learn.microsoft.com/ja-jp/dotnet/core/project-sdk/overview |
| nuget | dotnet package add | https://learn.microsoft.com/ja-jp/dotnet/core/tools/dotnet-package-add |
| debug | コンソールアプリのデバッグ | https://learn.microsoft.com/ja-jp/dotnet/core/tutorials/debugging-with-visual-studio-code |
| test | C#とxUnitの単体テスト | https://learn.microsoft.com/ja-jp/dotnet/core/testing/unit-testing-csharp-with-xunit |
| di | .NETの依存性注入 | https://learn.microsoft.com/ja-jp/dotnet/core/extensions/dependency-injection |
| http | HttpClientのガイドライン | https://learn.microsoft.com/ja-jp/dotnet/fundamentals/networking/http/httpclient-guidelines |
| http-request | HttpClientでHTTPリクエストを行う | https://learn.microsoft.com/ja-jp/dotnet/fundamentals/networking/http/httpclient |
| minimal | 最小APIの作成チュートリアル | https://learn.microsoft.com/ja-jp/aspnet/core/tutorials/min-web-api?view=aspnetcore-10.0 |
| responses | 最小APIの応答 | https://learn.microsoft.com/ja-jp/aspnet/core/fundamentals/minimal-apis/responses?view=aspnetcore-10.0 |
| asp-di | ASP.NET Coreの依存性注入 | https://learn.microsoft.com/ja-jp/aspnet/core/fundamentals/dependency-injection?view=aspnetcore-10.0 |
| config | ASP.NET Coreの構成 | https://learn.microsoft.com/ja-jp/aspnet/core/fundamentals/configuration/?view=aspnetcore-10.0 |
| integration | ASP.NET Coreの統合テスト | https://learn.microsoft.com/ja-jp/aspnet/core/test/integration-tests?view=aspnetcore-10.0 |
| secrets | 開発時のシークレット管理 | https://learn.microsoft.com/ja-jp/aspnet/core/security/app-secrets?view=aspnetcore-10.0 |
| csharp14 | C# 14 の新機能 | https://learn.microsoft.com/ja-jp/dotnet/csharp/whats-new/csharp-14 |
| package-add | dotnet package add コマンド | https://learn.microsoft.com/ja-jp/dotnet/core/tools/dotnet-package-add |
| http-guidelines | HttpClientの寿命・接続管理ガイドライン | https://learn.microsoft.com/ja-jp/dotnet/fundamentals/networking/http/httpclient-guidelines |
| gc | GCの基礎 | https://learn.microsoft.com/en-us/dotnet/standard/garbage-collection/fundamentals |
| managed | マネージ実行の流れ | https://learn.microsoft.com/en-us/dotnet/standard/managed-execution-process |
| aot | Native AOT | https://learn.microsoft.com/en-us/dotnet/core/deploying/native-aot/ |
| cancellation | 協調的キャンセル | https://learn.microsoft.com/en-us/dotnet/standard/threading/cancellation-in-managed-threads |
| binding | Minimal APIのパラメーターバインド | https://learn.microsoft.com/en-us/aspnet/core/fundamentals/minimal-apis/parameter-binding?view=aspnetcore-10.0 |
| middleware | ASP.NET Coreのミドルウェア | https://learn.microsoft.com/en-us/aspnet/core/fundamentals/middleware/?view=aspnetcore-10.0 |
| http-semantics | HTTP Semantics — RFC 9110 | https://www.rfc-editor.org/rfc/rfc9110.html |
| http-patch | PATCH Method for HTTP — RFC 5789 | https://www.rfc-editor.org/info/rfc5789/ |
| logging | ASP.NET Coreのログ | https://learn.microsoft.com/en-us/aspnet/core/fundamentals/logging/?view=aspnetcore-10.0 |
| http-factory | IHttpClientFactory | https://learn.microsoft.com/en-us/dotnet/core/extensions/httpclient-factory |
| boxing | ボックス化とボックス化解除 | https://learn.microsoft.com/en-us/dotnet/csharp/programming-guide/types/boxing-and-unboxing |
| struct | 構造体 | https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/builtin-types/struct |
| dispose | Disposeパターン | https://learn.microsoft.com/en-us/dotnet/standard/garbage-collection/implementing-dispose |
