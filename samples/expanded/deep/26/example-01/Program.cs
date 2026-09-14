int actual = ShippingFee(5000);
int expected = 0;
if (actual != expected)
{
    throw new InvalidOperationException($"期待:{expected} 実際:{actual}");
}
Console.WriteLine("境界5000の比較が一致");

static int ShippingFee(int subtotal)
{
    return subtotal >= 5000 ? 0 : 500;
}
