using System.Linq;

int[] scores = { 40, 80, 65, 90 };
var result = scores.Where(score => score >= 70);
Console.WriteLine(string.Join(", ", result));
