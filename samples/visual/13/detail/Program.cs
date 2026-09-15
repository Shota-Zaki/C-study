var first = new Basket(new List<string> { "ノート" });
var second = first;
second.Items.Add("ペン");
Console.WriteLine(first.Items.Count);
record struct Basket(List<string> Items);
