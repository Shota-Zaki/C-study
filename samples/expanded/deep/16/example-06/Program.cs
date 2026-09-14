int quantity = 0;
try
{
    quantity = int.Parse("abc");
}
catch (Exception)
{
}
Console.WriteLine($"数量={quantity}");
