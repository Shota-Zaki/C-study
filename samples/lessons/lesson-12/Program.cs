var service = new StudyService(new ConsoleSender());
service.Complete();

public interface IMessageSender
{
    void Send(string message);
}
public class ConsoleSender : IMessageSender
{
    public void Send(string message) => Console.WriteLine(message);
}
public class StudyService
{
    private readonly IMessageSender sender;
    public StudyService(IMessageSender sender) => this.sender = sender;
    public void Complete() => sender.Send("学習完了");
}
