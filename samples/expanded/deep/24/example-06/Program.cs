using System.Linq;

using var gate = new SemaphoreSlim(2);
int[] inputs = { 1, 2, 3, 4 };
Task<int>[] tasks = inputs.Select(ProcessAsync).ToArray();
int[] results = await Task.WhenAll(tasks);
Console.WriteLine(string.Join(",", results));

async Task<int> ProcessAsync(int value)
{
    await gate.WaitAsync();
    try
    {
        await Task.Delay(10);
        return value * 10;
    }
    finally
    {
        gate.Release();
    }
}
