using System.Linq;

var numbers = new List<int> { 1, 2, 3 };
IEnumerable<int> query = numbers.Where(number => number >= 2);
numbers.Add(4);
Console.WriteLine(string.Join(",", query));
numbers.Remove(2);
Console.WriteLine(string.Join(",", query));
