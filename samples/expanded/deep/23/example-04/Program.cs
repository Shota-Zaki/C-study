await SaveAsync();
Console.WriteLine("保存できました");

static async Task SaveAsync()
{
    await Task.Delay(10);
    Console.WriteLine("実際の保存処理が完了");
}
