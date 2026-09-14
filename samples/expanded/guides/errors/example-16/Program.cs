var stock = new Stock();
Console.WriteLine(stock.TryTake(2));
Console.WriteLine(stock.Count);
class Stock
{
    private int _count = 5;
    public int Count => _count;
    public bool TryTake(int amount)
    {
        if (amount <= 0 || amount > _count) return false;
        _count -= amount;
        return true;
    }
}
