int[] prices = { 100, 200, 300, 400 };
int[] result = prices.Where(p => p >= 200).Take(2).ToArray();
Console.WriteLine(string.Join(", ", result));
Console.WriteLine(prices.Length);
