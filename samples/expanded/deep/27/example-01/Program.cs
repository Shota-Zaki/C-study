int total = CalculateTotal(120, 3);
Console.WriteLine($"合計:{total}");

static int CalculateTotal(int unitPrice, int quantity)
{
    if (unitPrice < 0) throw new ArgumentOutOfRangeException(nameof(unitPrice));
    if (quantity <= 0) throw new ArgumentOutOfRangeException(nameof(quantity));
    return checked(unitPrice * quantity);
}
