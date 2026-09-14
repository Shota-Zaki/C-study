Shape[] shapes = { new Rectangle(3, 4), new Square(5) };
foreach (Shape shape in shapes)
{
    Console.WriteLine(shape.Area());
}

public abstract class Shape
{
    public abstract int Area();
}
public sealed class Rectangle : Shape
{
    private readonly int _width;
    private readonly int _height;
    public Rectangle(int width, int height)
    {
        _width = width;
        _height = height;
    }
    public override int Area() => _width * _height;
}
public sealed class Square : Shape
{
    private readonly int _side;
    public Square(int side) { _side = side; }
    public override int Area() => _side * _side;
}
