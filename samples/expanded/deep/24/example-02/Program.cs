var first = new TaskCompletionSource<int>(TaskCreationOptions.RunContinuationsAsynchronously);
var second = new TaskCompletionSource<int>(TaskCreationOptions.RunContinuationsAsynchronously);
Task<int[]> all = Task.WhenAll(first.Task, second.Task);
second.SetResult(20);
Console.WriteLine(all.IsCompleted);
first.SetResult(10);
Console.WriteLine(string.Join(",", await all));
