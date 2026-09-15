var line = new OrderLine(120, 3);
Console.WriteLine(line.Total);
class OrderLine
{
    public int Price { get; }
    public int Quantity { get; }
    public int Total => Price * Quantity;
    public OrderLine(int price, int quantity)
    {
        Price = price;
        Quantity = quantity;
    }
}
