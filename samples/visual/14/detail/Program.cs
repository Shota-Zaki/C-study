var a = new Team(new List<string> { "Aoi" });
var b = new Team(new List<string> { "Aoi" });
Console.WriteLine(a == b);
Console.WriteLine(a.Members.SequenceEqual(b.Members));
record Team(List<string> Members);
