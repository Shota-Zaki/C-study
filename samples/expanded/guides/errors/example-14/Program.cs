var counter = new Counter();
Console.WriteLine(counter.Read());
class Counter
{
    public int Value = 3;
    public int Read() => Value;
}
