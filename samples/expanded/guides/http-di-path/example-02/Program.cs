var service = new GreetingService(new FixedNameSource());
Console.WriteLine(service.Create());

interface INameSource
{
    string GetName();
}
class FixedNameSource : INameSource
{
    public string GetName() => "学習者";
}
class GreetingService
{
    private readonly INameSource _source;
    public GreetingService(INameSource source) { _source = source; }
    public string Create() => $"こんにちは、{_source.GetName()}";
}
