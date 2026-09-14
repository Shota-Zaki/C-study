if (!int.TryParse("abc", out int quantity))
{
    Console.WriteLine("数量の変換に失敗しました");
    return;
}
Console.WriteLine($"数量={quantity}");
