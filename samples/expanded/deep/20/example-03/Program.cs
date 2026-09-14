string input = "99";
if (Enum.TryParse<WorkStatus>(input, ignoreCase: true, out var status)
    && Enum.IsDefined(status))
{
    Console.WriteLine(status);
}
else
{
    Console.WriteLine("状態を確認してください");
}

public enum WorkStatus { Todo, Doing, Done }
