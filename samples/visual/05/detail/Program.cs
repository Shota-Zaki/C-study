foreach (int subtotal in new[] { 4999, 5000, 5001 })
{
    int shipping = subtotal >= 5000 ? 0 : 600;
    Console.WriteLine($"{subtotal}円 → 送料{shipping}円");
}
