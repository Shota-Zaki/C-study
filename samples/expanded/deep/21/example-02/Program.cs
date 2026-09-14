Console.WriteLine($"作業場所:{Environment.CurrentDirectory}");
Console.WriteLine($"アプリ基準:{AppContext.BaseDirectory}");
string path = Path.Combine(Environment.CurrentDirectory, "data", "items.json");
Console.WriteLine($"保存先:{Path.GetFullPath(path)}");
