var first = new Box { Value = 10 };
Box second = first;
second.Value = 20;
Console.WriteLine(first.Value);
Console.WriteLine(ReferenceEquals(first, second));

public class Box
{
    public int Value { get; set; }
}
