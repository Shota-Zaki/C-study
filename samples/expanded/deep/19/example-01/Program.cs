Console.WriteLine("A:列を取得");
IEnumerable<int> numbers = CreateNumbers();
Console.WriteLine("B:列挙を開始");
foreach (int number in numbers)
{
    Console.WriteLine($"受取:{number}");
}

static IEnumerable<int> CreateNumbers()
{
    Console.WriteLine("C:生成開始");
    yield return 10;
    Console.WriteLine("D:次へ進む");
    yield return 20;
}
