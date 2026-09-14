using System.Linq;

int[] scores = { 40, 80, 65, 90 };
IEnumerable<string> labels = scores.Select(score => $"{score}点");
Console.WriteLine(string.Join(" / ", labels));
