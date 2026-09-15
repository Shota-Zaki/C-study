int subtotal = 4200;
bool isMember = true;
int shipping;
if (subtotal >= 5000)
    shipping = 0;
else if (isMember)
    shipping = 300;
else
    shipping = 600;
Console.WriteLine($"送料: {shipping}円");
Console.WriteLine($"支払合計: {subtotal + shipping}円");
