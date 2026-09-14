using var reader = new StringReader("C#\n.NET\nWeb API");
string? line;
int lineNumber = 0;
while ((line = reader.ReadLine()) is not null)
{
    lineNumber++;
    Console.WriteLine($"{lineNumber}: {line}");
}
