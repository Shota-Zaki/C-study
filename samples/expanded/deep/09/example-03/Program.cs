var first = new Counter();
var second = new Counter();
first.Increment();
first.Increment();
second.Increment();
Console.WriteLine($"first={first.Value}, second={second.Value}");
Console.WriteLine($"全体={Counter.TotalIncrements}");

public class Counter
{
    public int Value { get; private set; }
    public static int TotalIncrements { get; private set; }

    public void Increment()
    {
        Value++;
        TotalIncrements++;
    }
}
