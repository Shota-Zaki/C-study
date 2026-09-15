using System.Text.Json;
var task = new TaskItem(1, "Review", false);
string json = JsonSerializer.Serialize(task);
Console.WriteLine(json);
TaskItem? restored = JsonSerializer.Deserialize<TaskItem>(json);
Console.WriteLine(restored?.Title ?? "復元なし");
record TaskItem(int Id, string Title, bool Done);
