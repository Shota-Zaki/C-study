using System.Globalization;

var started = new DateTimeOffset(2026, 9, 14, 9, 0, 0, TimeSpan.FromHours(9));
var ended = started.AddMinutes(45);
TimeSpan duration = ended - started;
Console.WriteLine(started.ToUniversalTime().ToString("yyyy-MM-dd HH:mm 'UTC'", CultureInfo.InvariantCulture));
Console.WriteLine($"{duration.TotalMinutes}分");
Console.WriteLine(1234.5m.ToString("F2", CultureInfo.InvariantCulture));
