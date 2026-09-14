using System.Text.Json;

string json = "{\"Name\":\"\",\"Quantity\":-5}";
ItemInput? item = JsonSerializer.Deserialize<ItemInput>(json);
if (item is null || string.IsNullOrWhiteSpace(item.Name) || item.Quantity <= 0)
{
    Console.WriteLine("名前と数量を確認してください");
    return;
}
Console.WriteLine($"{item.Name.Trim()}:{item.Quantity}");

public sealed class ItemInput
{
    public string? Name { get; set; }
    public int Quantity { get; set; }
}
