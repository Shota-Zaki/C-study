Console.WriteLine("開始");
string result = await GetMessageAsync();
Console.WriteLine(result);
Console.WriteLine("終了");

static async Task<string> GetMessageAsync()
{
    await Task.Delay(10);
    return "受信完了";
}
