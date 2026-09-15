var titles = new List<string>();
bool added = TryAdd(titles, "   ");
Console.WriteLine(added);
Console.WriteLine(titles.Count);
static bool TryAdd(List<string> target, string? title)
{
    if (string.IsNullOrWhiteSpace(title)) return false;
    target.Add(title.Trim());
    return true;
}
