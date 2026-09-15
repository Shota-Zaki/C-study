if (TryCalculate(" 3 ", 120m, out decimal total))
    Console.WriteLine($"合計: {total:0}円");
else
    Console.WriteLine("数量が不正です");
static bool TryCalculate(string input, decimal price, out decimal total)
{
    total = 0m;
    if (price < 0m || !int.TryParse(input, out int quantity) || quantity < 1)
        return false;
    total = price * quantity;
    return true;
}
