int result = CalculateTotal(120, 3);
Console.WriteLine(result);

static int CalculateTotal(int unitPrice, int quantity)
{
    int total = unitPrice * quantity;
    return total;
}
