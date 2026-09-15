using var source = new CancellationTokenSource();
source.Cancel();
try
{
    await Task.Delay(100, source.Token);
}
catch (OperationCanceledException)
{
    Console.WriteLine("中止を確認しました");
}
