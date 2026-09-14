var notebook = new Product("ノート", 200);
var pen = new Product("ペン", 100);
Console.WriteLine($"{notebook.Name}: {notebook.Price}");
Console.WriteLine($"{pen.Name}: {pen.Price}");

public class Product
{
    public string Name { get; }
    public int Price { get; }

    public Product(string name, int price)
    {
        Name = name;
        Price = price;
    }
}
