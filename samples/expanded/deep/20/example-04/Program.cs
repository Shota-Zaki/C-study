var result = Calculate(new[] { 10, 20, 30 });
Console.WriteLine($"件数:{result.Count}, 合計:{result.Total}");
(int count, int total) = Calculate(new[] { 4, 5 });
Console.WriteLine($"件数:{count}, 合計:{total}");

static (int Count, int Total) Calculate(int[] values)
{
    int total = 0;
    foreach (int value in values)
    {
        total += value;
    }
    return (values.Length, total);
}
