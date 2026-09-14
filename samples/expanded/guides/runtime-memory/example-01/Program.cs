int total = 10;
int result = Add(total, 5);
Console.WriteLine(total);
Console.WriteLine(result);

static int Add(int a, int b)
{
    a += b;
    return a;
}
