var notebook = new Product("ノート", 200);
var pen = new Product("ペン", 120);
Console.WriteLine($"{notebook.Name}: {notebook.Price}円");
Console.WriteLine($"{pen.Name}: {pen.Price}円");

class Product
{
    public string Name { get; }
    public int Price { get; }
    public Product(string name, int price)
    {
        Name = name;
        Price = price;
    }
}
