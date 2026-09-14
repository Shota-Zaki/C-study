var product = new Product("ノート", 200);
Console.WriteLine(product.Name);

public class Product
{
    public string Name { get; }
    public int Price { get; }

    public Product(string name, int price)
    {
        if (string.IsNullOrWhiteSpace(name))
            throw new ArgumentException("商品名が必要です", nameof(name));
        if (price < 0)
            throw new ArgumentOutOfRangeException(nameof(price));
        Name = name.Trim();
        Price = price;
    }
}
