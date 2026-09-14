using System.Linq;

int[] scores = Array.Empty<int>();
if (scores.Length == 0)
{
    Console.WriteLine("平均なし");
}
else
{
    Console.WriteLine(scores.Average());
}
