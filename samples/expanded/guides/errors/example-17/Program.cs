var a = new Item("本");
var b = new Item("本");
Console.WriteLine(a == b);
class Item
{
    public Item(string name) { Name = name; }
    public string Name { get; }
}
