decimal first = AddTax(1000m, 0.10m);
decimal second = AddTax(2500m, 0.10m);
Console.WriteLine($"{first:0}円");
Console.WriteLine($"{second:0}円");

static decimal AddTax(decimal price, decimal rate)
{
    return price * (1m + rate);
}
