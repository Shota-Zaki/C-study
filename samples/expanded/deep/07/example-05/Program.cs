int count = 5;
Increase(ref count);
Console.WriteLine(count);
bool success = int.TryParse("12", out int parsed);
Console.WriteLine($"{success}, {parsed}");

static void Increase(ref int value)
{
    value++;
}
