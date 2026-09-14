int? score = null;
if (score is int actualScore)
{
    Console.WriteLine(actualScore);
}
else
{
    Console.WriteLine("未受験");
}
