var service = new OrderService(new ConsoleNotifier());
service.Confirm("A001");
interface INotifier { void Send(string message); }
class ConsoleNotifier : INotifier
{
    public void Send(string message) => Console.WriteLine(message);
}
class OrderService
{
    private readonly INotifier notifier;
    public OrderService(INotifier notifier) { this.notifier = notifier; }
    public void Confirm(string id) => notifier.Send($"注文{id}を確定しました");
}
