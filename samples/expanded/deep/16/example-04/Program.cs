Process();

static void Process()
{
    using var resource = new TraceResource();
    Console.WriteLine("処理");
    return;
}

public sealed class TraceResource : IDisposable
{
    public TraceResource() { Console.WriteLine("生成"); }
    public void Dispose() { Console.WriteLine("解放処理"); }
}
