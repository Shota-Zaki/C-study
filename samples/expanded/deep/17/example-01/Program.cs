Func<int, int> operation = Double;
int result = operation(4);
Console.WriteLine(result);

static int Double(int value)
{
    return value * 2;
}
