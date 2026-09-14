var source = new[] { new Item { Name = "A", Count = 1 } };
Item[] shallow = (Item[])source.Clone();
shallow[0].Count = 9;
Console.WriteLine(source[0].Count);
Console.WriteLine(ReferenceEquals(source, shallow));
Console.WriteLine(ReferenceEquals(source[0], shallow[0]));

public class Item
{
    public string Name { get; set; } = "";
    public int Count { get; set; }
}
