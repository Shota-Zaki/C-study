string? name = null;
int length = name?.Length ?? 0;
Console.WriteLine(length);

name = "CSharp";
if (name is not null)
{
    Console.WriteLine(name.Length);
}
int? score = null;
Console.WriteLine(score ?? -1);
