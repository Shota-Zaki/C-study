using System.Text.Json;

string json = "{\"Name\":\"\",\"Quantity\":-5}";
Item? item = JsonSerializer.Deserialize<Item>(json);
Console.WriteLine(item?.Quantity);

public record Item(string Name, int Quantity);
