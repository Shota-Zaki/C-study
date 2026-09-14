using System.Diagnostics;

var watch = Stopwatch.StartNew();
long total = 0;
for (int i = 0; i < 100_000; i++)
{
    total += i;
}
watch.Stop();
Console.WriteLine(total);
Console.WriteLine($"計測ミリ秒:{watch.Elapsed.TotalMilliseconds}");
