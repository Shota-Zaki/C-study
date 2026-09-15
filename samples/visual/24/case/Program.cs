Task<int> first = LoadAsync(10, 30);
Task<int> second = LoadAsync(20, 10);
int[] results = await Task.WhenAll(first, second);
Console.WriteLine(string.Join(", ", results));
static async Task<int> LoadAsync(int value, int delay)
{
    await Task.Delay(delay);
    return value;
}
