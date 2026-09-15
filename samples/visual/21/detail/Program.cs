using System.Text.Json;
string json = "{broken}";
try
{
    _ = JsonSerializer.Deserialize<Dictionary<string, string>>(json);
}
catch (JsonException)
{
    Console.WriteLine("JSONの形式が不正です");
}
