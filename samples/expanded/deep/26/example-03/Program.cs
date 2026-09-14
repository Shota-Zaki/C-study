Console.WriteLine(ShippingFee(4999));
Console.WriteLine(ShippingFee(5000));
Console.WriteLine(ShippingFee(5001));

static int ShippingFee(int subtotal)
{
    return subtotal >= 5000 ? 0 : 500;
}
