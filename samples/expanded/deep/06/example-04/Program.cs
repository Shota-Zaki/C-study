int[] minutes = { 20, 0, 45, 10, 30 };
int activeDays = 0;
int total = 0;
foreach (int value in minutes)
{
    if (value == 0)
    {
        continue;
    }
    activeDays++;
    total += value;
}
Console.WriteLine($"学習日={activeDays}");
Console.WriteLine($"合計={total}");
