int[] scores = { 40, 80, 65, 90 };
var passing = new List<int>();
foreach (int score in scores)
{
    if (score >= 70)
    {
        passing.Add(score);
    }
}
Console.WriteLine(string.Join(", ", passing));
