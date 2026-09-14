WorkStatus status = (WorkStatus)99;
Console.WriteLine(status);
Console.WriteLine(Enum.IsDefined(status));

public enum WorkStatus { Todo, Doing, Done }
