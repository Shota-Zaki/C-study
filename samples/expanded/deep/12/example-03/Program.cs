var recorder = new RecordingNotifier();
var service = new ReportService(recorder);
service.Complete("在庫集計");
Console.WriteLine(recorder.LastMessage);

public interface INotifier
{
    void Send(string message);
}
public class RecordingNotifier : INotifier
{
    public string? LastMessage { get; private set; }
    public void Send(string message)
    {
        LastMessage = message;
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
