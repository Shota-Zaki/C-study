OrderStatus status = OrderStatus.Paid;
Console.WriteLine(status.ToLabel());
enum OrderStatus { Pending, Paid, Shipped }
static class OrderStatusExtensions
{
    public static string ToLabel(this OrderStatus status) => status switch
    {
        OrderStatus.Pending => "支払い待ち",
        OrderStatus.Paid => "支払い済み",
        OrderStatus.Shipped => "発送済み",
        _ => "不明な状態"
    };
}
