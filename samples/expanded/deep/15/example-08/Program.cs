var stock = new Dictionary<string, int>();
if (stock.TryGetValue("PEN", out int quantity))
    Console.WriteLine(quantity);
else
    Console.WriteLine("商品コードが未登録です");
