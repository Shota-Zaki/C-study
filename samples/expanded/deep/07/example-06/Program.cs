int[] prices = { 120, 250, 180 };
int subtotal = Sum(prices);
int discount = 50;
int payment = ApplyDiscount(subtotal, discount);
Console.WriteLine($"小計={subtotal}, 支払={payment}");

static int Sum(int[] values)
{
    int total = 0;
    foreach (int value in values) total += value;
    return total;
}

static int ApplyDiscount(int total, int discount)
{
    int result = total - discount;
    return result < 0 ? 0 : result;
}
