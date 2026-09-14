var products = new[]
{
    new Product("ノート", 200),
    new Product("本", 1200),
    new Product("ペン", 100)
};
var names = products
    .Where(p => p.Price <= 500)
    .OrderBy(p => p.Price)
    .Select(p => p.Name)
    .ToList();
Console.WriteLine(string.Join(", ", names));

public record Product(string Name, int Price);
