string input = "abc";
if (int.TryParse(input, out int quantity))
{
    Console.WriteLine(quantity * 120);
}
else
{
    Console.WriteLine("数量の形式が正しくありません");
}
