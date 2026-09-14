var result = Calculate();
Console.WriteLine($"件数:{result.Count}, 合計:{result.Total}");

static (int Count, int Total) Calculate()
{
    int count = 3;
    int total = 60;
    return (total, count);
}
