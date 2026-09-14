using System.Linq;

List<int> result = new[] { 1, 2, 3 }
    .Where(number => number >= 2)
    .ToList();
Console.WriteLine(result.Count);
Console.WriteLine(result.Sum());
