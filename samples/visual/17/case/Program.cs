Func<int, int> coupon = amount => Math.Max(0, amount - 100);
Func<int, int> tenPercent = amount => amount * 90 / 100;
int price = 1500;
Console.WriteLine(coupon(price));
Console.WriteLine(tenPercent(price));
