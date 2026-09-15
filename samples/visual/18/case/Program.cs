var products = new[]
{
    new Product("ノート", 200),
    new Product("ペン", 120),
    new Product("ファイル", 500)
};
string[] labels = products
    .Where(p => p.Price >= 200)
    .Select(p => $"{p.Name}: {p.Price}円")
    .ToArray();
foreach (string label in labels) Console.WriteLine(label);
record Product(string Name, int Price);
