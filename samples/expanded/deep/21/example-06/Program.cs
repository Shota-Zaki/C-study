using System.Text.Json;

string json = "{\"name\":\"Note\"}";
var exact = JsonSerializer.Deserialize<NameInput>(json);
var flexible = JsonSerializer.Deserialize<NameInput>(json,
    new JsonSerializerOptions { PropertyNameCaseInsensitive = true });
Console.WriteLine(exact?.Name ?? "未設定");
Console.WriteLine(flexible?.Name ?? "未設定");

public sealed class NameInput
{
    public string? Name { get; set; }
}
