var signal = new TaskCompletionSource<bool>(
    TaskCreationOptions.RunContinuationsAsynchronously);
Console.WriteLine("1:呼び出す前");
Task<string> work = ReadAfterSignalAsync(signal.Task);
Console.WriteLine("3:呼び出し元へ戻った");
signal.SetResult(true);
Console.WriteLine(await work);

static async Task<string> ReadAfterSignalAsync(Task signal)
{
    Console.WriteLine("2:最初のawaitより前");
    await signal;
    return "4:信号の後に完了";
}
