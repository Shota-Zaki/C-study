try
{
    int result = await LoadAsync();
    Console.WriteLine(result);
}
catch (InvalidOperationException ex)
{
    Console.WriteLine($"読み込み失敗:{ex.Message}");
}

static async Task<int> LoadAsync()
{
    await Task.Delay(1);
    throw new InvalidOperationException("形式が不正です");
}
