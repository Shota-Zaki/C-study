using System.Globalization;
var date = new DateOnly(2026, 1, 1);
string label = date.ToString("yyyy-MM-dd", CultureInfo.InvariantCulture);
Console.WriteLine($"{label}: 集計完了");
