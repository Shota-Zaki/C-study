Console.WriteLine("開始");
try
{
    Console.WriteLine("変換前");
    int value = int.Parse("abc");
    Console.WriteLine(value);
}
catch (FormatException)
{
    Console.WriteLine("整数の形式ではありません");
}
finally
{
    Console.WriteLine("後片付け");
}
Console.WriteLine("終了");
