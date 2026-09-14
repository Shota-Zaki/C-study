var values = new List<int> { 1, 2, 3, 4 };
values.RemoveAll(value => value % 2 == 0);
Console.WriteLine(string.Join(",", values));
