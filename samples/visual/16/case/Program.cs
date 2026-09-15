using System.IO;
using (var reader = new StringReader("ノート\nペン"))
{
    string? line;
    while ((line = reader.ReadLine()) is not null)
        Console.WriteLine(line);
}
Console.WriteLine("読み取り終了");
