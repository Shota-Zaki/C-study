var signal = new TaskCompletionSource<int>();
Console.WriteLine("1:呼び出し前");
Task work = ObserveAsync(signal.Task);
Console.WriteLine("3:まだ合図していない");
signal.SetResult(7);
await work;
Console.WriteLine("5:観察が完了");

static async Task ObserveAsync(Task<int> source)
{
    Console.WriteLine("2:待機の直前");
    int value = await source;
    Console.WriteLine($"4:結果は{value}");
}
