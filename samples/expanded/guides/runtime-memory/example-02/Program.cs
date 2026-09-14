int first = 3;
int second = first;
second = 9;

var a = new List<int> { 3 };
var b = a;
b.Add(9);
Console.WriteLine($"{first}/{second}");
Console.WriteLine(string.Join(",", a));
