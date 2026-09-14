using System.Linq;

int[] scores = { 60, 80, 100 };
Console.WriteLine(scores.Any(score => score < 60));
Console.WriteLine(scores.Sum());
Console.WriteLine(scores.Average());
Console.WriteLine(scores.Max());
