var stock = new StockService(5);
HandleInput("2", stock);
HandleInput("10", stock);
HandleInput("abc", stock);
Console.WriteLine($"最終在庫:{stock.Count}");

static void HandleInput(string text, StockService stock)
{
    if (!int.TryParse(text, out int quantity))
    {
        Console.WriteLine("整数で入力してください");
        return;
    }
    TakeResult result = stock.Take(quantity);
    Console.WriteLine(result.Message);
}

public record TakeResult(bool Accepted, string Message);

public sealed class StockService
{
    public int Count { get; private set; }
    public StockService(int count)
    {
        if (count < 0) throw new ArgumentOutOfRangeException(nameof(count));
        Count = count;
    }
    public TakeResult Take(int quantity)
    {
        if (quantity <= 0) return new(false, "数量は1以上です");
        if (quantity > Count) return new(false, "在庫不足です");
        Count -= quantity;
        return new(true, $"{quantity}個を受け付けました");
    }
}
