Console.WriteLine("開始");
string result = await LoadAsync();
Console.WriteLine(result);
Console.WriteLine("終了");
static async Task<string> LoadAsync()
{
    await Task.Delay(20);
    return "取得完了";
}
