var unspecified = new DateTime(2026, 9, 14, 9, 0, 0);
var utc = new DateTime(2026, 9, 14, 0, 0, 0, DateTimeKind.Utc);
Console.WriteLine(unspecified.Kind);
Console.WriteLine(utc.Kind);
