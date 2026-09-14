var stock = new Dictionary<string, int>(StringComparer.OrdinalIgnoreCase)
{
    ["PEN"] = 5,
    ["BOOK"] = 2
};
stock["PEN"] = stock["PEN"] - 1;
if (stock.TryGetValue("pen", out int quantity))
{
    Console.WriteLine(quantity);
}
Console.WriteLine(stock.TryGetValue("CLIP", out _));
