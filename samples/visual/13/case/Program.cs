var original = new List<string> { "ノート" };
var shared = original;
var copied = new List<string>(original);
shared.Add("ペン");
Console.WriteLine(string.Join(", ", original));
Console.WriteLine(string.Join(", ", copied));
Console.WriteLine(ReferenceEquals(original, shared));
Console.WriteLine(ReferenceEquals(original, copied));
