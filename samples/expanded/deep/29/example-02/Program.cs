var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

app.MapGet("/items/{id:int}", (int id) =>
{
    return Results.Ok(new Item(id, $"Item-{id}"));
});

app.Run();

public record Item(int Id, string Name);
