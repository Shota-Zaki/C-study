TaskState state = TaskState.Doing;
Console.WriteLine(state);
var (count, total) = Summarize(new[] { 10, 20 });
Console.WriteLine($"{count}件 / {total}");
Console.WriteLine("C#".HasText());

static (int Count, int Total) Summarize(int[] values)
    => (values.Length, values.Sum());

public enum TaskState { Todo = 0, Doing = 1, Done = 2 }
public static class TextExtensions
{
    public static bool HasText(this string? value)
        => !string.IsNullOrWhiteSpace(value);
}
