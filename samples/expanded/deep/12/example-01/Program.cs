INotifier notifier = new ConsoleNotifier();
notifier.Send("保存しました");

public interface INotifier
{
    void Send(string message);
}
public class ConsoleNotifier : INotifier
{
    public void Send(string message)
    {
        Console.WriteLine($"通知: {message}");
    }
}
