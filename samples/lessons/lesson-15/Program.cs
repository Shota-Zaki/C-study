var scores = new Dictionary<string, int>
{
    ["C#"] = 80,
    ["SQL"] = 90
};
if (scores.TryGetValue("C#", out int score))
    Console.WriteLine(score);

var tags = new HashSet<string> { "C#", "SQL", "C#" };
Console.WriteLine(tags.Count);
Console.WriteLine(First(new[] { 10, 20 }));

static T First<T>(T[] values)
{
    if (values.Length == 0) throw new ArgumentException("要素が必要です");
    return values[0];
}
