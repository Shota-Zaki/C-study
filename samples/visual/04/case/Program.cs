string[] inputs = { "3", "0", "abc" };
foreach (string input in inputs)
{
    if (!int.TryParse(input, out int quantity))
        Console.WriteLine($"{input}: 整数を入力してください");
    else if (quantity < 1)
        Console.WriteLine($"{input}: 1以上を入力してください");
    else
        Console.WriteLine($"{input}: {quantity}個を受け付けました");
}
