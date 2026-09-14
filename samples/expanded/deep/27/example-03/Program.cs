var stock = new Stock(3);
Console.WriteLine(stock.Take(5));
Console.WriteLine(stock.Count);

public sealed class Stock
{
    public int Count { get; private set; }
    public Stock(int count) => Count = count;
    public bool Take(int quantity)
    {
        Count -= quantity;
        if (Count < 0) return false;
        return true;
    }
}
