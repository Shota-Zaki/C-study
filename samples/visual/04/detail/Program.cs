string input = "  SAVE  ";
string command = input.Trim();
bool isSave = string.Equals(command, "save", StringComparison.OrdinalIgnoreCase);
Console.WriteLine(command);
Console.WriteLine(isSave);
