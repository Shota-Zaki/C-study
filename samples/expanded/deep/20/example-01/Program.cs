WorkStatus status = WorkStatus.Todo;
Console.WriteLine(status);
status = WorkStatus.Doing;
Console.WriteLine(status);
status = WorkStatus.Done;
Console.WriteLine((int)status);

public enum WorkStatus
{
    Todo = 0,
    Doing = 1,
    Done = 2
}
