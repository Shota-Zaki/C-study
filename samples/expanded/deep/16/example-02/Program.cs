try
{
    Console.WriteLine(ReadQuantity("abc"));
}
catch (FormatException)
{
    Console.WriteLine("数量を入力し直してください");
}

static int ReadQuantity(string input)
{
    return int.Parse(input);
}
