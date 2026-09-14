using System.Text.Json;

string directory = Path.Combine(Environment.CurrentDirectory, "practice-data");
Directory.CreateDirectory(directory);
string path = Path.Combine(directory, "items.json");
var items = new List<Item>
{
    new Item("Note", 3),
    new Item("Pen", 2)
};
var options = new JsonSerializerOptions { WriteIndented = true };
string json = JsonSerializer.Serialize(items, options);
File.WriteAllText(path, json);

string saved = File.ReadAllText(path);
List<Item>? loaded = JsonSerializer.Deserialize<List<Item>>(saved);
if (loaded is null)
{
    Console.WriteLine("一覧がnullです");
    return;
}
foreach (Item item in loaded)
{
    Console.WriteLine($"{item.Name}:{item.Quantity}");
}

public record Item(string Name, int Quantity);
