foreach (string? title in new string?[] { null, "  ", "Review", new string('A', 101) })
{
    string? normalized = title?.Trim();
    bool valid = !string.IsNullOrEmpty(normalized) && normalized.Length <= 100;
    Console.WriteLine(valid);
}
