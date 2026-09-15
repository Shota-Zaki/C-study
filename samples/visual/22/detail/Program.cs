using System.Globalization;
decimal value = 1234.5m;
Console.WriteLine(value.ToString("0.00", CultureInfo.InvariantCulture));
Console.WriteLine(value.ToString("N2", CultureInfo.InvariantCulture));
