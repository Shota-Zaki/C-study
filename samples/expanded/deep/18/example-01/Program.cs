int[] scores = { 40, 80, 65, 90 };
var passing = new List<int>();
for (int i = 0; i < scores.Length; i++)
{
    if (scores[i] >= 70)
    {
        passing.Add(scores[i]);
    }
}
Console.WriteLine(string.Join(", ", passing));
