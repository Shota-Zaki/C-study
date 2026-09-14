using System.Globalization;

string input = "2026-09-14";
bool ok = DateOnly.TryParseExact(input, "yyyy-MM-dd",
    CultureInfo.InvariantCulture, DateTimeStyles.None, out DateOnly date);
if (ok)
{
    Console.WriteLine(date.ToString("yyyy-MM-dd", CultureInfo.InvariantCulture));
}
else
{
    Console.WriteLine("日付は年-月-日で入力してください");
}
