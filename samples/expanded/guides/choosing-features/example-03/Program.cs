int value = 3;
Replace(ref value);
Console.WriteLine(value);
static void Replace(ref int target)
{
    target = 8;
}
