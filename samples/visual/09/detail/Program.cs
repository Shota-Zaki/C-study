try { _ = new Product(-1); }
catch (ArgumentOutOfRangeException) { Console.WriteLine("価格が不正です"); }
class Product
{
    public int Price { get; }
    public Product(int price)
    {
        if (price < 0) throw new ArgumentOutOfRangeException(nameof(price));
        Price = price;
    }
}
