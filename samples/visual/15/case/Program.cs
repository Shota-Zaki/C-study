var prices = new Dictionary<string, int>
{
    ["P01"] = 200,
    ["P02"] = 120
};
foreach (string code in new[] { "P01", "P99" })
{
    if (prices.TryGetValue(code, out int price))
        Console.WriteLine($"{code}: {price}円");
    else
        Console.WriteLine($"{code}: 未登録");
}
