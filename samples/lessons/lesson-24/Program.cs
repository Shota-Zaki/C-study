Task<int> first = LoadAsync(10);
Task<int> second = LoadAsync(20);
int[] results = await Task.WhenAll(first, second);
Console.WriteLine(results.Sum());

using var source = new CancellationTokenSource();
source.Cancel();
try
{
    await Task.Delay(100, source.Token);
}
catch (OperationCanceledException) when (source.IsCancellationRequested)
{
    Console.WriteLine("キャンセルしました");
}
static async Task<int> LoadAsync(int value)
{
    await Task.Delay(20);
    return value;
}
