string[] commands = { "save", "load", "save", "SAVE", "load" };
var counts = new Dictionary<string, int>(StringComparer.OrdinalIgnoreCase);
foreach (string command in commands)
{
    counts.TryGetValue(command, out int current);
    counts[command] = current + 1;
}
Console.WriteLine($"save={counts["save"]}");
Console.WriteLine($"load={counts["load"]}");
