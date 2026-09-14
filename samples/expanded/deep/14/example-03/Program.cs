var original = new Basket(new List<string> { "Pen" });
var copied = original with { };
copied.Items.Add("Book");
Console.WriteLine(string.Join(",", original.Items));
Console.WriteLine(ReferenceEquals(original.Items, copied.Items));

public record Basket(List<string> Items);
