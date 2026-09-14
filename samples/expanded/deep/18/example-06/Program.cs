using System.Linq;

Order[] orders =
{
    new Order(1, "ノート", 2, true),
    new Order(2, "ペン", 1, false),
    new Order(3, "付箋", 3, true)
};
List<string> shipping = orders
    .Where(order => order.IsPaid)
    .Select(order => $"注文{order.Id}:{order.Name}×{order.Quantity}")
    .ToList();
foreach (string line in shipping)
{
    Console.WriteLine(line);
}

public record Order(int Id, string Name, int Quantity, bool IsPaid);
