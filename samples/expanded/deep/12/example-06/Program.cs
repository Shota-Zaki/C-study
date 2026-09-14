INotifier notifier = new ConsoleNotifier();
notifier.Send("確認");

public interface INotifier
{
    void Send(string message);
}
public class ConsoleNotifier : INotifier
{
    void INotifier.Send(string message)
    {
        Console.WriteLine(message);
    }
}
