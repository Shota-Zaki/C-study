using System.IO;
using (var reader = new StringReader("一行目\n二行目"))
{
    Console.WriteLine(reader.ReadLine());
    Console.WriteLine(reader.ReadLine());
}
Console.WriteLine("読み取り終了");
