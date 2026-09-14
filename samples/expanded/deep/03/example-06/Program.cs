using System.Globalization;

decimal unitPrice = 198.5m;
int quantity = 3;
decimal subtotal = unitPrice * quantity;
decimal tax = Math.Round(subtotal * 0.10m, 0, MidpointRounding.AwayFromZero);
decimal total = subtotal + tax;
Console.WriteLine(subtotal.ToString("F1", CultureInfo.InvariantCulture));
Console.WriteLine(tax.ToString("F0", CultureInfo.InvariantCulture));
Console.WriteLine(total.ToString("F1", CultureInfo.InvariantCulture));
