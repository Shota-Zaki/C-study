var names = new Dictionary<int, string>();
names.Add(10, "ノート");
names.Add(20, "ペン");
if (names.TryGetValue(20, out string? name))
{
    Console.WriteLine(name);
}
var processed = new HashSet<int>();
Console.WriteLine(processed.Add(20));
Console.WriteLine(processed.Add(20));
