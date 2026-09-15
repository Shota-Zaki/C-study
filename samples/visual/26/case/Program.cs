var cases = new[] { (Price: 4999, Expected: 600), (Price: 5000, Expected: 0), (Price: 5001, Expected: 0) };
foreach (var item in cases)
{
    int actual = Shipping(item.Price);
    string result = actual == item.Expected ? "PASS" : "FAIL";
    Console.WriteLine($"{item.Price}: {result}");
}
static int Shipping(int price) => price >= 5000 ? 0 : 600;
