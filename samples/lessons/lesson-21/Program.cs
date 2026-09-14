using System.Text.Json;

var session = new StudyLog("CSharp", 30);
string json = JsonSerializer.Serialize(session);
Console.WriteLine(json);
var restored = JsonSerializer.Deserialize<StudyLog>(json)
    ?? throw new InvalidOperationException("データがありません");
Console.WriteLine(restored.Minutes);

public record StudyLog(string Subject, int Minutes);
