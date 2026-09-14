using System.Linq;

IEnumerable<int> query = new[] { 1, 2, 3 }.Where(number =>
{
    Console.WriteLine($"判定:{number}");
    return number >= 2;
});
Console.WriteLine(query.Count());
Console.WriteLine(query.Sum());
