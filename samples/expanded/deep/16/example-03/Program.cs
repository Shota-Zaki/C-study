Console.WriteLine("外側の開始");
using (var resource = new TraceResource())
{
    Console.WriteLine("利用中");
}
Console.WriteLine("外側の続き");

public sealed class TraceResource : IDisposable
{
    public TraceResource() { Console.WriteLine("生成"); }
    public void Dispose() { Console.WriteLine("解放処理"); }
}
