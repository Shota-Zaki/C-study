using var source = new CancellationTokenSource();
source.Cancel();
try
{
    await Task.Delay(1000, source.Token);
}
catch (OperationCanceledException)
{
    Console.WriteLine("中止されました");
}
