var original = new Product("Pen", 100);
var discounted = original with { Price = 80 };
Console.WriteLine($"{original.Name}:{original.Price}");
Console.WriteLine($"{discounted.Name}:{discounted.Price}");
Console.WriteLine(ReferenceEquals(original, discounted));

public record Product(string Name, int Price);
