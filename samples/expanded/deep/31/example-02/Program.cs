var builder = WebApplication.CreateBuilder(args);
builder.Services.AddSingleton<IClock, SystemClock>();
builder.Services.AddScoped<GreetingService>();
var app = builder.Build();

app.MapGet("/greeting", (GreetingService service) =>
    Results.Ok(new { message = service.Create() }));

app.Run();

public interface IClock
{
    DateTimeOffset UtcNow { get; }
}
public sealed class SystemClock : IClock
{
    public DateTimeOffset UtcNow => DateTimeOffset.UtcNow;
}
public sealed class GreetingService
{
    private readonly IClock _clock;
    public GreetingService(IClock clock) => _clock = clock;
    public string Create() => $"UTC年:{_clock.UtcNow.Year}";
}
