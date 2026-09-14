Func<int, int> doubleValue = x => x * 2;
Action<string> log = message => Console.WriteLine(message);
log($"結果: {doubleValue(4)}");

int factor = 2;
Func<int, int> multiply = x => x * factor;
factor = 3;
Console.WriteLine(multiply(4));
