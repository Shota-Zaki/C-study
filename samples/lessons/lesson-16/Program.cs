using var reader = new StringReader("C#\n.NET");
Console.WriteLine(reader.ReadLine());

try
{
    int value = int.Parse("not-a-number");
    Console.WriteLine(value);
}
catch (FormatException)
{
    Console.WriteLine("整数として読めませんでした");
}
