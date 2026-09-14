var values = new List<int> { 1, 2, 3 };
var query = values.Where(x => x >= 2);
var snapshot = query.ToList();
values.Add(4);
Console.WriteLine(string.Join(",", query));
Console.WriteLine(string.Join(",", snapshot));
Console.WriteLine(query.Sum());
