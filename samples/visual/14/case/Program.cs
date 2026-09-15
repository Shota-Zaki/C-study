var original = new Product(1, "ノート", 200);
var same = new Product(1, "ノート", 200);
var updated = original with { Price = 220 };
Console.WriteLine(original == same);
Console.WriteLine(ReferenceEquals(original, same));
Console.WriteLine($"変更前: {original.Price}円");
Console.WriteLine($"変更後: {updated.Price}円");
record Product(int Id, string Name, int Price);
