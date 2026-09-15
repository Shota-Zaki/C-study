int stock = 10;
int remaining = SellOne(stock);
Console.WriteLine($"元: {stock}");
Console.WriteLine($"戻り値: {remaining}");
static int SellOne(int value)
{
    value--;
    return value;
}
