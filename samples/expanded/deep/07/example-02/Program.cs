int score = 10;
Increase(score);
Console.WriteLine(score);

static void Increase(int value)
{
    value += 5;
    Console.WriteLine(value);
}
