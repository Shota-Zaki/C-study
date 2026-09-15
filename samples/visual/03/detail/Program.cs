decimal unitPrice = 105m;
int quantity = 2;
decimal perItem = decimal.Floor(unitPrice * 1.10m) * quantity;
decimal perOrder = decimal.Floor(unitPrice * quantity * 1.10m);
Console.WriteLine($"商品ごと: {perItem}");
Console.WriteLine($"注文全体: {perOrder}");
