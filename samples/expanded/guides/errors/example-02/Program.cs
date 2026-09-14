string input = "3";
if (int.TryParse(input, out int count))
{
    Console.WriteLine(count + 1);
}
else
{
    Console.WriteLine("整数を入力してください");
}
