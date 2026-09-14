Task all = Task.WhenAll(FailAsync("A"), FailAsync("B"));
try
{
    await all;
}
catch
{
    int count = all.Exception?.InnerExceptions.Count ?? 0;
    Console.WriteLine($"失敗件数:{count}");
}

static async Task FailAsync(string name)
{
    await Task.Delay(1);
    throw new InvalidOperationException(name);
}
