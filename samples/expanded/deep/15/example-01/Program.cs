var numbers = new List<int> { 1, 2, 3 };
numbers.Add(4);
numbers.Remove(2);
numbers[0] = 10;
Console.WriteLine(string.Join(",", numbers));
Console.WriteLine(numbers.Count);
