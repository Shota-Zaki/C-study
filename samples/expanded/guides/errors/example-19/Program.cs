var values = new List<int> { 1, 2 };
var query = values.Where(n => n >= 2);
values.Add(3);
Console.WriteLine(string.Join(",", query));
