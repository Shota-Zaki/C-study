int limit = 60;
Func<int, bool> isPassing = score => score >= limit;
Console.WriteLine(isPassing(70));
limit = 80;
Console.WriteLine(isPassing(70));
