var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();
app.MapPost("/tasks/validate", (CreateTask request) =>
{
    if (string.IsNullOrWhiteSpace(request.Title))
        return Results.ValidationProblem(new Dictionary<string, string[]>
        {
            ["title"] = new[] { "タイトルは必須です" }
        });
    return Results.Ok(new { title = request.Title.Trim() });
});
app.Run();
record CreateTask(string? Title);
