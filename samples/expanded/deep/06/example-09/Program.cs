int[] scores = { 40, 80, 60, 90 };
int count = 0;
int total = 0;
foreach (int score in scores)
{
    if (score >= 60)
    {
        count++;
        total += score;
    }
}
Console.WriteLine($"件数={count}, 合計={total}");
