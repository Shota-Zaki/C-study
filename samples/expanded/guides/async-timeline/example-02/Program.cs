var first = new TaskCompletionSource<int>();
var second = new TaskCompletionSource<int>();
Task<int[]> all = Task.WhenAll(first.Task, second.Task);
second.SetResult(20);
Console.WriteLine(all.IsCompleted);
first.SetResult(10);
int[] result = await all;
Console.WriteLine(string.Join(",", result));
