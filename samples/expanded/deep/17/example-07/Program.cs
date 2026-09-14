var stock = new Stock();
Action<int> handler = remaining => Console.WriteLine($"残り:{remaining}");
stock.Changed += handler;
stock.TakeOne();
stock.Changed -= handler;
stock.TakeOne();
Console.WriteLine($"最終:{stock.Count}");

public sealed class Stock
{
    public int Count { get; private set; } = 3;
    public event Action<int>? Changed;

    public void TakeOne()
    {
        if (Count == 0) return;
        Count--;
        Changed?.Invoke(Count);
    }
}
