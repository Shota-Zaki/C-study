bool rejected = false;
try { _ = SquareRoot(-1); }
catch (ArgumentOutOfRangeException) { rejected = true; }
Console.WriteLine(rejected ? "PASS" : "FAIL");
static double SquareRoot(double value)
{
    if (value < 0) throw new ArgumentOutOfRangeException(nameof(value));
    return Math.Sqrt(value);
}
