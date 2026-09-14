string input = "3";
if (!int.TryParse(input, out int quantity) || quantity <= 0)
{
    Console.WriteLine("個数は正の整数です");
    return;
}
decimal total = OrderCalculator.Total(500m, quantity);
Console.WriteLine($"合計: {total}");

public static class OrderCalculator
{
    public static decimal Total(decimal price, int quantity)
    {
        if (price < 0m) throw new ArgumentOutOfRangeException(nameof(price));
        if (quantity <= 0) throw new ArgumentOutOfRangeException(nameof(quantity));
        return price * quantity;
    }
}
