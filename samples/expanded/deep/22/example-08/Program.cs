using System.Globalization;

var date = new DateOnly(2026, 9, 14);
date = date.AddDays(1);
Console.WriteLine(date.ToString("yyyy-MM-dd", CultureInfo.InvariantCulture));
