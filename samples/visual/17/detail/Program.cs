int discount = 100;
Func<int, int> apply = price => price - discount;
discount = 200;
Console.WriteLine(apply(1000));
