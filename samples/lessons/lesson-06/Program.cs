int[] scores = { 70, 85, 90 };
int sum = 0;
foreach (int score in scores)
{
    sum += score;
}
Console.WriteLine($"人数: {scores.Length}");
Console.WriteLine($"合計: {sum}");
