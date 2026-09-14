int morningMinutes = 25;
int eveningMinutes = 40;
int totalMinutes = morningMinutes + eveningMinutes;
int goalMinutes = 90;
int remainingMinutes = goalMinutes - totalMinutes;
Console.WriteLine($"合計: {totalMinutes}分");
Console.WriteLine($"目標まで: {remainingMinutes}分");
