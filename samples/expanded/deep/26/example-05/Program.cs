var stock = new Stock(3);
bool accepted = stock.TryTake(2);
Check(accepted, "2個の要求が通る");
Check(stock.Count == 1, "残数は1");
bool rejected = stock.TryTake(2);
Check(!rejected, "不足時は拒否");
Check(stock.Count == 1, "拒否時も残数は1");
Console.WriteLine("4つの比較が一致");

static void Check(bool condition, string description)
{
    if (!condition) throw new InvalidOperationException(description);
}

public sealed class Stock
{
    public int Count { get; private set; }
    public Stock(int count)
    {
        if (count < 0) throw new ArgumentOutOfRangeException(nameof(count));
        Count = count;
    }
    public bool TryTake(int quantity)
    {
        if (quantity <= 0 || quantity > Count) return false;
        Count -= quantity;
        return true;
    }
}
