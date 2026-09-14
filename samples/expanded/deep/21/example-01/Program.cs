using System.Text.Json;

var item = new Item("Note", 3);
string json = JsonSerializer.Serialize(item);
Console.WriteLine(json);
Item? loaded = JsonSerializer.Deserialize<Item>(json);
if (loaded is null)
{
    Console.WriteLine("データなし");
}
else
{
    Console.WriteLine($"{loaded.Name}:{loaded.Quantity}");
}

public record Item(string Name, int Quantity);
