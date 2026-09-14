var item = new LineItem(120, 3);
Console.WriteLine(item.UnitPrice);
Console.WriteLine(item.Quantity);
Console.WriteLine(item.Total);

public class LineItem
{
    public int UnitPrice { get; }
    public int Quantity { get; }
    public int Total => UnitPrice * Quantity;

    public LineItem(int unitPrice, int quantity)
    {
        UnitPrice = unitPrice;
        Quantity = quantity;
    }
}
