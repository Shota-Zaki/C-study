using System.Linq;

int[] scores = { 40, 80, 65, 90 };
IEnumerable<int> passing = scores.Where(score => score >= 70);
Console.WriteLine(string.Join(", ", passing));
