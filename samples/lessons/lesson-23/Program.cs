Console.WriteLine("開始");
string result = await LoadMessageAsync();
Console.WriteLine(result);
Console.WriteLine("完了");

static async Task<string> LoadMessageAsync()
{
    await Task.Delay(30); // 待ち時間を学習用に再現する。
    return "読み込み結果";
}
