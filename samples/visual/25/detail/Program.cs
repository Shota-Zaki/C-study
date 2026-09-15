// 同じプロジェクトの別ファイルへ分割することもできます。
Console.WriteLine(PriceCalculator.AddTax(1000));
static class PriceCalculator
{
    public static int AddTax(int price) => price * 110 / 100;
}
