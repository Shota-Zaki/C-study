using System.Globalization;

var japan = new DateTimeOffset(2026, 9, 14, 9, 0, 0, TimeSpan.FromHours(9));
DateTimeOffset utc = japan.ToUniversalTime();
Console.WriteLine(japan.ToString("yyyy-MM-dd HH:mm zzz", CultureInfo.InvariantCulture));
Console.WriteLine(utc.ToString("yyyy-MM-dd HH:mm zzz", CultureInfo.InvariantCulture));
Console.WriteLine(japan == utc);
