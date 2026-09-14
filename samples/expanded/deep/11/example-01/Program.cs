Shape shape = new Rectangle(3, 4);
Console.WriteLine(shape.Area());

public class Shape
{
    public virtual int Area() => 0;
}

public class Rectangle : Shape
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
