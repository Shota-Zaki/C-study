string?[] names = { null, "", "   ", " Aoi " };
foreach (string? name in names)
{
    string display = string.IsNullOrWhiteSpace(name)
        ? "ゲスト"
        : name.Trim();
    Console.WriteLine(display);
}
