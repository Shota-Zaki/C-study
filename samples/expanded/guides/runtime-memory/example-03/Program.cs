var original = new Basket(new List<string> { "本" });
var copied = original;
copied.Items.Add("ペン");
Console.WriteLine(string.Join(",", original.Items));

readonly record struct Basket(List<string> Items);
