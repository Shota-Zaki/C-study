var first = new Position(2, 3);
var moved = first with { X = 5 };
Console.WriteLine($"{first.X},{first.Y}");
Console.WriteLine($"{moved.X},{moved.Y}");
Console.WriteLine(first == new Position(2, 3));
readonly record struct Position(int X, int Y);
