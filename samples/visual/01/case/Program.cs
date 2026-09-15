int minutesPerDay = 25;
int days = 5;
int totalMinutes = minutesPerDay * days;
int hours = totalMinutes / 60;
int minutes = totalMinutes % 60;
Console.WriteLine($"合計: {totalMinutes}分");
Console.WriteLine($"{hours}時間{minutes}分");
