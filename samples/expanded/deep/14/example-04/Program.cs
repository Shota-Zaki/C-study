var original = new Basket(new List<string> { "Pen" });
var copied = original with { Items = new List<string>(original.Items) };
copied.Items.Add("Book");
Console.WriteLine(string.Join(",", original.Items));
Console.WriteLine(string.Join(",", copied.Items));
public record Basket(List<string> Items);
