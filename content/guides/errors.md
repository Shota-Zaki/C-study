## エラーを四つの段階へ分ける

「動かない」という情報だけでは原因を選べません。環境の問題、コンパイル時の問題、実行中の例外、期待値と違う論理の問題に分けます。例外は実行中の失敗を通常の戻り値とは別に伝える仕組みで、コンパイルエラーはそもそも実行用の成果物を作れない問題です。

| 段階 | 例 | 最初に確認するもの |
|---|---|---|
| 環境・起動 | dotnetがない、対象SDKがない | SDK一覧、カレントディレクトリ、設定 |
| コンパイル | 名前がない、型が違う、かっこが足りない | 最初の診断、ファイル名、行、直前の構文 |
| 実行中 | null参照、範囲外、読み込み失敗 | 例外の型、メッセージ、最初の自分の行 |
| 論理 | 割引が違う、更新されない、二重作成 | 入力、期待値、途中状態、変更した順序 |

診断の番号は有用ですが、番号を丸暗記してから直す必要はありません。まず「何の操作が、どんな値に対して行われたか」を記録します。多数のエラーが出たときは、最初の引用符や波かっこの欠落を直すと後続が消える場合があります。最後の行だけを無作為に直さないようにします。

## 01：型が違う値を代入する

目的は注文数を整数として保存することです。次の例では文字列をintへ直接入れようとしています。

```csharp-error
int count = "3";
Console.WriteLine(count);
```

起きることはコンパイルエラーです。確認位置はcountの宣言の右辺で、引用符付きの"3"は文字列です。数字に見える文字と数値の型は別です。入力が固定値なら`int count = 3;`へ修正します。外から文字列で届くなら、変換の成功を確認してから利用します。

```csharp
string input = "3";
if (int.TryParse(input, out int count))
{
    Console.WriteLine(count + 1);
}
else
{
    Console.WriteLine("整数を入力してください");
}
```

期待される出力は4です。入力を`abc`にすれば案内を表示し、countを注文処理へ渡しません。防止策は、表示用の文字列と計算用の型の境界を決め、TryParseの戻り値を無視しないことです。[Lesson 04](../lessons/04.html)で入力と業務条件を分けます。

## 02：整数除算の後で型を変える

目的は5を2で割った2.5を求めることです。次のコードはビルドできても、計算の順序が目的に合いません。

```csharp
int total = 5;
int count = 2;
double average = total / count;
Console.WriteLine(average == 2);
```

期待される表示はTrueです。右辺はint同士なので、先に整数として2を作り、その2をdoubleへ変換します。確認箇所は代入先ではなく割り算の両側の型です。修正位置は右辺で、割る前に片方をdoubleへ変換します。

```csharp
int total = 5;
int count = 2;
double average = (double)total / count;
Console.WriteLine(average == 2.5);
```

修正後も表示はTrueですが、今度の比較対象は2.5です。状態表に「演算の型」と「代入の型」を別々に書くと原因を見失いません。countが0のケースは別途契約を決めます。整数除算はゼロ除算で例外になり、浮動小数点の除算とは規則が異なるので同一視しません。

## 03：nullの参照先を読もうとする

```csharp-error
string? name = null;
Console.WriteLine(name!.Length);
```

起きることはNullReferenceExceptionです。`!`は警告の解析へ意図を伝えるだけで、nullを文字列へ置き換えません。確認位置はLengthの直前の値で、Lengthへ到達するための実体がありません。入力なしを拒否するか、欠損として処理するかを決めます。

```csharp
string? name = null;
if (name is null)
{
    Console.WriteLine("名前が未指定です");
}
else
{
    Console.WriteLine(name.Length);
}
```

期待される出力は名前が未指定です。nullと空文字を区別する仕様なら、安易に`?? ""`でまとめません。防止策は、参照を受け取る境界で欠損を表現し、使用する前に必要な条件を確認することです。[Lesson 08](../lessons/08.html)で`?.`と`??`の違いも扱います。

## 04：最後の添字を要素数と間違える

```csharp-error
int[] values = { 10, 20, 30 };
for (int i = 0; i <= values.Length; i++)
{
    Console.WriteLine(values[i]);
}
```

0、1、2の位置は読めますが、iが3になるとIndexOutOfRangeExceptionです。Lengthは要素数3であり、最後の位置は2です。確認位置は条件式と、values[i]のiです。修正は`<=`を`<`へ変えることです。

```csharp
int[] values = { 10, 20, 30 };
for (int i = 0; i < values.Length; i++)
{
    Console.WriteLine(values[i]);
}
```

期待される出力は10、20、30です。空配列ならi=0の時点で0<0がfalseになり一度も入りません。防止策は、添字が不要な表示にはforeachを使い、添字が必要な場合は0件・1件・複数件を確認することです。Listの不正な添字で発生する例外型は配列と同じとは限らないため、実際の型と診断を読みます。

## 05：continueで更新行を飛ばす

次は**起動しない失敗例**です。無限ループを観察するために端末やCPUを使い続ける必要はありません。状態表でiが変わらないことを確かめます。

```csharp-error
int i = 0;
while (i < 3)
{
    if (i == 1) continue;
    Console.WriteLine(i);
    i++;
}
```

最初は0を表示してiが1になります。その後はcontinueがi++を飛ばし、iが1のまま条件へ戻ります。確認箇所は「全ての経路でループを終了へ近づける値が変わるか」です。修正例では更新式を持つforにして、continueでも次の更新へ進む形にします。

```csharp
for (int i = 0; i < 3; i++)
{
    if (i == 1) continue;
    Console.WriteLine(i);
}
```

期待される出力は0、2です。防止策は、continue・break・returnの各経路を矢印で描くことです。既に誤って起動した場合、コンソールでは通常Ctrl+Cで中断を試せますが、全ての環境で即時終了を保証するものではありません。

## 06：参照の代入を独立コピーと考える

```csharp
var original = new List<int> { 1, 2 };
var backup = original;
original.Add(3);
Console.WriteLine(backup.Count);
```

期待される出力は3です。退避したつもりのbackupも同じListを参照しています。確認箇所は、独立した実体を作るnewやコピー処理を行ったかです。修正は`new List<int>(original)`で要素をコピーした別のListを作ることです。

```csharp
var original = new List<int> { 1, 2 };
var backup = new List<int>(original);
original.Add(3);
Console.WriteLine(backup.Count);
```

修正後は2です。この例は要素がintなので独立した値として扱えます。要素が変更可能なclassならListを複製しても各要素の参照先は共有されるため、必要なコピーの深さを別に検討します。防止策は、変数と実体の数を分けて図示することです。

## 07：staticから個別の状態を直接読む

```csharp-error
Console.WriteLine(Counter.Read());
class Counter
{
    public int Value = 3;
    public static int Read() => Value;
}
```

Valueは各Counterの状態ですが、staticのReadにはどのCounterかという対象がありません。コンパイル時にインスタンスが必要なことを指摘されます。修正位置はReadの契約と呼び出し側です。個別の状態を読むなら、インスタンスメソッドとして呼びます。

```csharp
var counter = new Counter();
Console.WriteLine(counter.Read());
class Counter
{
    public int Value = 3;
    public int Read() => Value;
}
```

期待される出力は3です。エラーを消すために全フィールドへstaticを付けると、今度は全対象で状態を共有してしまいます。防止策は「誰の値か」を決めてからstaticかinstanceかを選ぶことです。

## 08：privateの意味を無視して直接書き換える

```csharp-error
var stock = new Stock();
stock._count = -1;
class Stock
{
    private int _count = 5;
}
```

起きることはアクセスできないというコンパイルエラーです。確認箇所は宣言元のアクセス修飾子で、privateは外部から自由に触る契約ではありません。単にpublicへ変えると在庫が負数になる問題を許します。必要な操作を定義し、条件を守る形へ修正します。

```csharp
var stock = new Stock();
Console.WriteLine(stock.TryTake(2));
Console.WriteLine(stock.Count);
class Stock
{
    private int _count = 5;
    public int Count => _count;
    public bool TryTake(int amount)
    {
        if (amount <= 0 || amount > _count) return false;
        _count -= amount;
        return true;
    }
}
```

期待される出力はTrue、3です。先に条件を調べてから更新し、読む入口と変える入口を区別しています。防止策はエラーの回避を目的に公開範囲を広げず、外部へ許す操作から設計することです。

## 09：等しい内容と同じ実体を混ぜる

```csharp
var a = new Item("本");
var b = new Item("本");
Console.WriteLine(a == b);
class Item
{
    public Item(string name) { Name = name; }
    public string Name { get; }
}
```

期待される出力はFalseです。このclassには値比較を定義しておらず、別々に作った実体です。確認位置は型の等値性の契約です。名前の文字列だけを比較したいなら`a.Name == b.Name`、データ全体を値として比較する型ならrecordなどが候補です。

```csharp
var a = new Item("本");
var b = new Item("本");
Console.WriteLine(a == b);
Console.WriteLine(ReferenceEquals(a, b));
record Item(string Name);
```

期待される出力はTrue、Falseです。内容が等しいことと同じ実体であることを別々に検査しています。class・string・record・struct全てで`==`とEqualsが同じ規則だと暗記せず、型が何を比較しているかを確認します。

## 10：Whereを作った瞬間に結果が固定されると思う

```csharp
var values = new List<int> { 1, 2 };
var query = values.Where(n => n >= 2);
values.Add(3);
Console.WriteLine(string.Join(",", query));
```

期待される出力は`2,3`です。Whereは通常、列挙されるときに条件を評価します。確認箇所はToListなどで結果を保存した時点があるかです。定義時点の結果を保持する修正は、追加前に具象化することです。

```csharp
var values = new List<int> { 1, 2 };
var snapshot = values.Where(n => n >= 2).ToList();
values.Add(3);
Console.WriteLine(string.Join(",", snapshot));
```

修正後は2です。防止策は、クエリ定義、元の変更、列挙を別の行として追うことです。Selectで条件式を書けばboolの列になるなど、操作名と途中の型の誤解は[Lesson 18](../lessons/18.html)と[Lesson 19](../lessons/19.html)で確認します。

## 11：Taskを受け取らず終了する

```csharp-error
ShowAsync();
Console.WriteLine("メイン終了");
static async Task ShowAsync()
{
    await Task.Delay(100);
    Console.WriteLine("保存相当の処理が完了");
}
```

この例は呼び出しを待機しておらず、完了表示が出る前にプロセスが終わる可能性があります。表示順を確定値として扱わず、完了が追跡されていないことを問題にします。確認箇所は、返されたTaskを誰がawaitし、失敗を誰が受け取るかです。

```csharp
await ShowAsync();
Console.WriteLine("メイン終了");
static async Task ShowAsync()
{
    await Task.Delay(100);
    Console.WriteLine("保存相当の処理が完了");
}
```

修正後は完了の表示、メイン終了の順です。非同期メソッドは開始したことと終わったことを区別します。防止策は戻り値Taskを無視しないことと、async voidを通常の業務メソッドへ広げないことです。

## 12：例外を消して成功扱いする

```csharp-error
bool saved = false;
try
{
    throw new IOException("保存先へ書き込めません");
}
catch
{
    saved = true;
}
Console.WriteLine(saved);
```

起きることは、保存していないのにTrueを表示することです。catchは失敗を解決した証明ではありません。確認箇所は、状態変更と成功の意味が一致しているかです。修正例では失敗を明示して成功へ進ませません。

```csharp
bool saved = false;
try
{
    throw new IOException("保存先へ書き込めません");
}
catch (IOException)
{
    Console.WriteLine("保存に失敗しました。入力は保持します。");
}
Console.WriteLine(saved);
```

期待される出力は案内とFalseです。実際の業務では例外をどの境界へ伝えるかも決めます。再送が二重更新になる処理は、catchして無条件にやり直すだけでは安全になりません。

## 13：HTTPの失敗とJSONの失敗を混ぜる

HTTPは要求と応答の規則です。ステータスコードは結果の分類で、JSONは本文のデータ形式です。404の本文がHTMLだったとき、正常な商品DTOへ変換しようとするとJSON変換のエラーになり、元の不在という状況を見失う場合があります。

確認順は、①相手へ到達したか、②HTTP応答コードは何か、③本文の形式は想定どおりか、④型へ変換できるか、⑤変換後の値が業務条件を満たすか、です。[Lesson 28の失敗例と修正版](../deep-dives/28.html)では、実ネットワークを使わない偽ハンドラーで404と不正JSONを分けて扱います。実ネットワークのDNSやTLSが確認できたという意味ではありません。

## 修正を完了とする確認

直した一行を見て終わらず、同じ入力で期待値へ変わったことと、隣の境界で正しいことを確認します。修正前の失敗を捕まえるテストを残すと、後で同じ問題を戻した場合にも気づけます。これを回帰テストと呼びます。

記録は「入力→期待値→実際の結果→原因→修正位置→修正後の根拠→追加で試す条件」の順にします。ビルドや起動を行っていない場合は未検証とし、目視で正しそうなことを成功へ置き換えません。教材のコードも、この作業環境ではSDKを利用できていないため実ビルド・実行は未検証です。
