string? input = "25";
bool success = int.TryParse(input, out int quantity);
Console.WriteLine(success);
Console.WriteLine(quantity);
