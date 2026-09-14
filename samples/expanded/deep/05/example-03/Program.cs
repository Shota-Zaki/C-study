int age = 12;
if (age < 0 || age > 120)
{
    Console.WriteLine("年齢の範囲を確認してください");
    return;
}
int fee;
if (age < 6)
{
    fee = 0;
}
else if (age < 18)
{
    fee = 500;
}
else
{
    fee = 1000;
}
Console.WriteLine($"料金: {fee}円");
