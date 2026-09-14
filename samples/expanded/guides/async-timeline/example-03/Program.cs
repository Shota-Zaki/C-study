try
{
    await FailAsync();
}
catch (InvalidOperationException)
{
    Console.WriteLine("処理の失敗を受け取りました");
}

static async Task FailAsync()
{
    await Task.Yield();
    throw new InvalidOperationException("学習用の失敗");
}
