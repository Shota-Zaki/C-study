var original = new List<int> { 1, 2 };
var backup = original;
original.Add(3);
Console.WriteLine(backup.Count);
