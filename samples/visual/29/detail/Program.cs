Console.WriteLine(FindName(1) ?? "見つかりません");
Console.WriteLine(FindName(9) ?? "見つかりません");
static string? FindName(int id) => id == 1 ? "Notebook" : null;
