decimal unitPrice = 198m;
int quantity = 3;
const decimal TaxRate = 0.10m;
decimal subtotal = unitPrice * quantity;
decimal total = decimal.Floor(subtotal * (1m + TaxRate));
Console.WriteLine($"小計: {subtotal}円");
Console.WriteLine($"税込: {total}円");
