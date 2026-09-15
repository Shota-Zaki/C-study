var service = new ReportService(new FixedClock());
Console.WriteLine(service.Build());
interface IClock { DateTimeOffset UtcNow { get; } }
class FixedClock : IClock
{
    public DateTimeOffset UtcNow => new(2026, 1, 1, 0, 0, 0, TimeSpan.Zero);
}
class ReportService
{
    private readonly IClock clock;
    public ReportService(IClock clock) { this.clock = clock; }
    public string Build() => $"作成日: {clock.UtcNow:yyyy-MM-dd}";
}
