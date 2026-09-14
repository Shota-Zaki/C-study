using System.Globalization;

if (args.Length == 0)
{
    Console.WriteLine("使い方: dotnet run -- 食費:500 食費:800 交通費:200");
    return 0;
}
if (args.Length > 1000)
{
    Console.Error.WriteLine("1回に指定できる支出は1000件までです。");
    return 1;
}
var expenses = new List<Expense>();
foreach (string arg in args)
{
    int separator = arg.LastIndexOf(':');
    if (separator <= 0 || separator == arg.Length - 1)
    {
        Console.Error.WriteLine($"形式が不正です: {arg}（カテゴリ:金額で指定）");
        return 1;
    }
    string category = arg[..separator].Trim();
    string amountText = arg[(separator + 1)..];
    if (category.Length is < 1 or > 40 ||
        !decimal.TryParse(amountText, NumberStyles.AllowDecimalPoint,
            CultureInfo.InvariantCulture, out decimal amount) ||
        amount <= 0m || amount > 1_000_000_000m ||
        decimal.Round(amount, 2) != amount)
    {
        Console.Error.WriteLine($"入力が不正です: {arg}（カテゴリ1〜40文字、金額0超〜10億、小数2桁以内）");
        return 1;
    }
    expenses.Add(new Expense(category, amount));
}
foreach (var group in expenses.GroupBy(x => x.Category).OrderBy(g => g.Key, StringComparer.Ordinal))
    Console.WriteLine($"{group.Key}: {Format(group.Sum(x => x.Amount))}円");
Console.WriteLine($"合計: {Format(expenses.Sum(x => x.Amount))}円");
return 0;

static string Format(decimal value) => value.ToString("0.##", CultureInfo.InvariantCulture);
public record Expense(string Category, decimal Amount);

