string?[] inputs = { null, "", "   ", "  Aoi  " };
foreach (string? input in inputs)
{
    Console.WriteLine(GetDisplayName(input));
}

static string GetDisplayName(string? input)
{
    if (string.IsNullOrWhiteSpace(input))
    {
        return "匿名";
    }
    return input.Trim();
}
