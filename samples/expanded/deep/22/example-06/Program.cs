var today = new DateOnly(2026, 9, 14);
var deadline = new DateOnly(2026, 9, 20);
int remaining = deadline.DayNumber - today.DayNumber;
Console.WriteLine($"残り{remaining}日");
