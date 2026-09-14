string first = new string(new[] { 'A', 'B' });
string second = new string(new[] { 'A', 'B' });
Console.WriteLine(first == second);
object left = first;
object right = second;
Console.WriteLine(left == right);
Console.WriteLine(left.Equals(right));
