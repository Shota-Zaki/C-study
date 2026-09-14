var builder = WebApplication.CreateBuilder(args);
builder.Services.AddSingleton<VisitCounter>();
var app = builder.Build();
app.MapGet("/visits", (VisitCounter counter, ILogger<VisitCounter> logger) =>
{
    int count = counter.Next();
    logger.LogInformation("Visit count: {Count}", count);
    return Results.Ok(new { count });
});
app.Run("http://127.0.0.1:5080");

public class VisitCounter
{
    private int count;
    public int Next() => Interlocked.Increment(ref count);
}
