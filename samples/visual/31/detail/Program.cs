var service = new PriceService(price => price + 100);
Console.WriteLine(service.Total(500));
class PriceService
{
    private readonly Func<int, int> calculate;
    public PriceService(Func<int, int> calculate) { this.calculate = calculate; }
    public int Total(int price) => calculate(price);
}
