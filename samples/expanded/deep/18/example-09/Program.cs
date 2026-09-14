using System.Linq;

int[] numbers = { 3, 1, 2 };
var sorted = numbers.OrderBy(number => number).ToArray();
Console.WriteLine(string.Join(",", numbers));
Console.WriteLine(string.Join(",", sorted));
