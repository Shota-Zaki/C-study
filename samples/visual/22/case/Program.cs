using System.Globalization;
var utc = new DateTimeOffset(2026, 1, 1, 0, 0, 0, TimeSpan.Zero);
var local = utc.ToOffset(TimeSpan.FromHours(9));
Console.WriteLine(utc.ToString("yyyy-MM-dd HH:mm zzz", CultureInfo.InvariantCulture));
Console.WriteLine(local.ToString("yyyy-MM-dd HH:mm zzz", CultureInfo.InvariantCulture));
Console.WriteLine(utc == local);
