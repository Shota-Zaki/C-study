var inventory = new Inventory();
inventory.Add(3);
Console.WriteLine(inventory.Count);

public class Inventory
{
    public int Count { get; private set; }
    public void Add(int amount)
    {
        if (amount <= 0)
            throw new ArgumentOutOfRangeException(nameof(amount));
        Count += amount;
    }
}
