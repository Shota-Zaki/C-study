int[] minutes = { 120, 90, 150 };
int total = 0;
int longDays = 0;
foreach (int value in minutes)
{
    total += value;
    if (value >= 100) longDays++;
}
Console.WriteLine($"合計: {total}分");
Console.WriteLine($"100分以上: {longDays}日");
