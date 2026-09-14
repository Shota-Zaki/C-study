Console.WriteLine(FormatScore(null));
Console.WriteLine(FormatScore(0));
Console.WriteLine(FormatScore(80));

static string FormatScore(int? score)
{
    return score is int value ? $"{value}点" : "未受験";
}
