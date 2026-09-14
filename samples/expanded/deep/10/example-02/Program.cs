var stock = new Stock(5);
Console.WriteLine(stock.TryTake(2));
Console.WriteLine(stock.Quantity);
Console.WriteLine(stock.TryTake(10));
Console.WriteLine(stock.Quantity);

public class Stock
{
    public int Quantity { get; private set; }

    public Stock(int quantity)
    {
        if (quantity < 0)
            throw new ArgumentOutOfRangeException(nameof(quantity));
        Quantity = quantity;
    }

    public bool TryTake(int amount)
    {
        if (amount <= 0 || amount > Quantity)
            return false;
        Quantity -= amount;
        return true;
    }
}
