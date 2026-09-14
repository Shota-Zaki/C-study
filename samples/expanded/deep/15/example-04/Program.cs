var numberBox = new Box<int>(10);
var nameBox = new Box<string>("Aoi");
Console.WriteLine(numberBox.Value);
Console.WriteLine(nameBox.Value);

public class Box<T>
{
    public T Value { get; }
    public Box(T value)
    {
        Value = value;
    }
}
