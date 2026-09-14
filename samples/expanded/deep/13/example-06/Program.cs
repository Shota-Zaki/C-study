var source = new[] { new Item { Name = "A", Count = 1 } };
Item[] independent = new Item[source.Length];
for (int i = 0; i < source.Length; i++)
{
    independent[i] = new Item { Name = source[i].Name, Count = source[i].Count };
}
independent[0].Count = 9;
Console.WriteLine(source[0].Count);
Console.WriteLine(independent[0].Count);
public class Item
{
    public string Name { get; set; } = "";
    public int Count { get; set; }
}
