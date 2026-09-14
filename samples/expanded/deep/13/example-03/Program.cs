var first = new Box { Value = 10 };
Box second = first;
second.Value = 20;
second = new Box { Value = 30 };
Console.WriteLine($"first={first.Value}, second={second.Value}");
Console.WriteLine(ReferenceEquals(first, second));
public class Box
{
    public int Value { get; set; }
}
