int[] minutes = { 20, 35, 15 };
int total = 0;
for (int i = 0; i < minutes.Length; i++)
{
    total += minutes[i];
    Console.WriteLine($"i={i}, total={total}");
}
Console.WriteLine($"合計={total}");
