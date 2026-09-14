var first = new ProductClass("Pen", 100);
var second = new ProductClass("Pen", 100);
Console.WriteLine(first == second);
Console.WriteLine(first.Equals(second));

var one = new ProductRecord("Pen", 100);
var two = new ProductRecord("Pen", 100);
Console.WriteLine(one == two);
Console.WriteLine(ReferenceEquals(one, two));

public class ProductClass
{
    public string Name { get; }
    public int Price { get; }
    public ProductClass(string name, int price)
    {
        Name = name;
        Price = price;
    }
}
public record ProductRecord(string Name, int Price);
