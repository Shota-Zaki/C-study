int number = 10;
object boxed = number;
number = 20;
int restored = (int)boxed;
Console.WriteLine(restored);
long widened = (int)boxed;
Console.WriteLine(widened);
