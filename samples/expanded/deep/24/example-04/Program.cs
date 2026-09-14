using var source = new CancellationTokenSource();
source.Cancel();
try
{
    await LoadAsync(source.Token);
}
catch (OperationCanceledException) when (source.IsCancellationRequested)
{
    Console.WriteLine("中止しました");
}

static async Task LoadAsync(CancellationToken token)
{
    token.ThrowIfCancellationRequested();
    await Task.Delay(100, token);
    Console.WriteLine("完了");
}
