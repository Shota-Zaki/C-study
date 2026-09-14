var first = new Point { X = 1 };
var second = first;
second.X = 9;
Console.WriteLine(first.X);

var a = new Counter { Value = 1 };
var b = a;
b.Value = 9;
Console.WriteLine(a.Value);

public struct Point { public int X { get; set; } }
public class Counter { public int Value { get; set; } }
