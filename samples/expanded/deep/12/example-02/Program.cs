var service = new ReportService(new ConsoleNotifier());
service.Complete("売上集計");

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
public class ReportService
{
    private readonly INotifier _notifier;

    public ReportService(INotifier notifier)
    {
        _notifier = notifier;
    }

    public void Complete(string reportName)
    {
        _notifier.Send($"{reportName}が完了しました");
    }
}
