var stock = new Stock(5);
Console.WriteLine(stock.TryShip(3));
Console.WriteLine(stock.TryShip(9));
Console.WriteLine(stock.Quantity);
class Stock
{
    public int Quantity { get; private set; }
    public Stock(int quantity)
    {
        if (quantity < 0) throw new ArgumentOutOfRangeException(nameof(quantity));
        Quantity = quantity;
    }
    public bool TryShip(int amount)
    {
        if (amount <= 0 || amount > Quantity) return false;
        Quantity -= amount;
        return true;
    }
}
