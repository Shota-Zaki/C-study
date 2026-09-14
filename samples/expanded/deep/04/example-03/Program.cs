Console.Write("数量を入力: ");
string? input = Console.ReadLine();
if (!int.TryParse(input, out int quantity))
{
    Console.WriteLine("整数を入力してください");
    return;
}
if (quantity < 1 || quantity > 100)
{
    Console.WriteLine("数量は1〜100で入力してください");
    return;
}
int total = quantity * 120;
Console.WriteLine($"合計: {total}円");
