var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();
app.MapPost("/preview", Preview);
app.Run("http://127.0.0.1:5080");

static IResult Preview(CreateTaskRequest input)
{
    if (string.IsNullOrWhiteSpace(input.Title) || input.Title.Length > 100)
        return Results.BadRequest(new { error = "Titleは1〜100文字です" });
    return Results.Ok(new { title = input.Title.Trim() });
}
public record CreateTaskRequest(string? Title);
