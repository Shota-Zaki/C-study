string text = "  C#  ";
Console.WriteLine(text.NormalizeLabel());
Console.WriteLine(LabelExtensions.NormalizeLabel(text));

public static class LabelExtensions
{
    public static string NormalizeLabel(this string value)
    {
        ArgumentNullException.ThrowIfNull(value);
        return value.Trim();
    }
}
