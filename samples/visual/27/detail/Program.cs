Console.WriteLine(NormalizeTitle("  レビュー  "));
Console.WriteLine(NormalizeTitle("   ") ?? "入力エラー");
static string? NormalizeTitle(string? input)
{
    if (string.IsNullOrWhiteSpace(input)) return null;
    return input.Trim();
}
