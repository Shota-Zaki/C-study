using System.Linq;

int[] scores = { 40, 80, 65, 90 };
List<string> labels = scores
    .Where(score => score >= 70)
    .OrderByDescending(score => score)
    .Select(score => $"合格:{score}点")
    .ToList();
Console.WriteLine(string.Join(" / ", labels));
