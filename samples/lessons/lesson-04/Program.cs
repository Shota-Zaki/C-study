string raw = " 24 ";
if (int.TryParse(raw.Trim(), out int hours) && hours >= 0)
{
    Console.WriteLine($"今月は{hours}時間学習");
}
else
{
    Console.WriteLine("0以上の整数を入力してください");
}
Console.WriteLine("C#" == new string(new[] { 'C', '#' }));
