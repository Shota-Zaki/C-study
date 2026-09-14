Func<int, int> operation = value => value * 2;
Console.WriteLine(operation(4));

Func<int, int, int> add = (left, right) => left + right;
Console.WriteLine(add(3, 5));

Action<string> report = message => Console.WriteLine(message);
report("集計完了");
