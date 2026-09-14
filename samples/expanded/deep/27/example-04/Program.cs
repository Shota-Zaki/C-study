var stock = new Stock(3);
Console.WriteLine(stock.Take(5));
Console.WriteLine(stock.Count);

public sealed class Stock
{
    public int Count { get; private set; }
    public Stock(int count)
    {
        if (count < 0) throw new ArgumentOutOfRangeException(nameof(count));
        Count = count;
    }
    public bool Take(int quantity)
    {
        if (quantity <= 0 || quantity > Count) return false;
        Count -= quantity;
        return true;
    }
}
