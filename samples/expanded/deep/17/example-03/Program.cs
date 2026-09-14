int[] scores = { 40, 70, 85 };
Console.WriteLine(CountMatching(scores, score => score >= 60));
Console.WriteLine(CountMatching(scores, score => score >= 80));

static int CountMatching(int[] values, Func<int, bool> condition)
{
    int count = 0;
    foreach (int value in values)
    {
        if (condition(value))
        {
            count++;
        }
    }
    return count;
}
