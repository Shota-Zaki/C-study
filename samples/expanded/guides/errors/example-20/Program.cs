var values = new List<int> { 1, 2 };
var snapshot = values.Where(n => n >= 2).ToList();
values.Add(3);
Console.WriteLine(string.Join(",", snapshot));
