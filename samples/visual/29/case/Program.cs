var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();
app.MapGet("/health", () => Results.Ok(new { status = "ok" }));
app.MapGet("/products/{id:int}", (int id) =>
    id == 1
        ? Results.Ok(new { id = 1, name = "Notebook" })
        : Results.NotFound());
app.Run();
