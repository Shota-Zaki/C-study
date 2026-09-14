var a = new Scores(new[] { 80, 90 });
var b = new Scores(new[] { 80, 90 });
Console.WriteLine(a == b);
Console.WriteLine(a.Values.SequenceEqual(b.Values));

public record Scores(int[] Values);
