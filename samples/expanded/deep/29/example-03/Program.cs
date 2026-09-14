var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

app.MapGet("/greet", (string? name) =>
{
    string label = string.IsNullOrWhiteSpace(name) ? "Guest" : name.Trim();
    return Results.Ok(new { message = $"Hello, {label}" });
});

app.Run();
