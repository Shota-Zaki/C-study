int value = int.MaxValue;
try
{
    int next = checked(value + 1);
    Console.WriteLine(next);
}
catch (OverflowException)
{
    Console.WriteLine("intの範囲を超えました");
}
