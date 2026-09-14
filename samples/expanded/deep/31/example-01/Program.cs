var service = new GreetingService(new FixedClock());
Console.WriteLine(service.Create());

public interface IClock
{
    DateTimeOffset UtcNow { get; }
}
public sealed class FixedClock : IClock
{
    public DateTimeOffset UtcNow => new(2026, 9, 14, 0, 0, 0, TimeSpan.Zero);
}
public sealed class GreetingService
{
    private readonly IClock _clock;
    public GreetingService(IClock clock)
    {
        _clock = clock ?? throw new ArgumentNullException(nameof(clock));
    }
    public string Create() => $"UTC年:{_clock.UtcNow.Year}";
}
