#nullable enable
string? name = null;
if (name is null)
{
    Console.WriteLine("名前がありません");
}
else
{
    Console.WriteLine(name.Length);
}
