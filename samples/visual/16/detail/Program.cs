try
{
    using var resource = new DemoResource();
    throw new InvalidOperationException();
}
catch (InvalidOperationException) { Console.WriteLine("catch"); }
class DemoResource : IDisposable
{
    public void Dispose() => Console.WriteLine("Dispose");
}
