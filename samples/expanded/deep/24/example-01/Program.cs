Task<int> first = LoadAsync(10);
Task<int> second = LoadAsync(20);
int[] results = await Task.WhenAll(first, second);
Console.WriteLine(string.Join(",", results));

static async Task<int> LoadAsync(int value)
{
    await Task.Delay(10);
    return value;
}
