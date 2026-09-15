Notification[] items = { new EmailNotification(), new ScreenNotification() };
foreach (Notification item in items) item.Send("発送完了");
abstract class Notification
{
    public abstract void Send(string message);
}
class EmailNotification : Notification
{
    public override void Send(string message) => Console.WriteLine($"メール: {message}");
}
class ScreenNotification : Notification
{
    public override void Send(string message) => Console.WriteLine($"画面: {message}");
}
