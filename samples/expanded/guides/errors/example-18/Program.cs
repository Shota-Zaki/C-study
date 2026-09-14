var a = new Item("本");
var b = new Item("本");
Console.WriteLine(a == b);
Console.WriteLine(ReferenceEquals(a, b));
record Item(string Name);
