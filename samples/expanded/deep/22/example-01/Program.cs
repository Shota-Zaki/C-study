using System.Globalization;

var deadline = new DateOnly(2026, 9, 30);
DateOnly next = deadline.AddDays(1);
Console.WriteLine(deadline.ToString("yyyy-MM-dd", CultureInfo.InvariantCulture));
Console.WriteLine(next.ToString("yyyy-MM-dd", CultureInfo.InvariantCulture));
