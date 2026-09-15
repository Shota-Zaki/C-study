string input = "99";
bool parsed = Enum.TryParse(input, out OrderStatus status);
Console.WriteLine(parsed);
Console.WriteLine(Enum.IsDefined(status));
enum OrderStatus { Pending, Paid, Shipped }
