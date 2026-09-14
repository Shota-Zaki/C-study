var first = new Result("C#", 80);
var second = new Result("C#", 80);
var improved = first with { Score = 95 };
Console.WriteLine(first == second);
Console.WriteLine(ReferenceEquals(first, second));
Console.WriteLine($"{first.Score} → {improved.Score}");

public record Result(string Subject, int Score);
