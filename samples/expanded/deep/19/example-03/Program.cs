using System.Linq;

var numbers = new List<int> { 1, 2, 3 };
List<int> snapshot = numbers.Where(number => number >= 2).ToList();
numbers.Add(4);
Console.WriteLine(string.Join(",", snapshot));
Console.WriteLine(string.Join(",", numbers));
