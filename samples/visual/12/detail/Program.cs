var notifier = new RecordingNotifier();
notifier.Send("発送完了");
Console.WriteLine(notifier.LastMessage);
interface INotifier { void Send(string message); }
class RecordingNotifier : INotifier
{
    public string? LastMessage { get; private set; }
    public void Send(string message) { LastMessage = message; }
}
