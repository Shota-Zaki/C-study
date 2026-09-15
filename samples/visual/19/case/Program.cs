var numbers = new List<int> { 1, 2, 3 };
var query = numbers.Where(n => n % 2 == 0);
var snapshot = query.ToList();
numbers.Add(4);
Console.WriteLine($"再評価: {string.Join(", ", query)}");
Console.WriteLine($"保存済み: {string.Join(", ", snapshot)}");
