var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

app.MapPost("/validate-title", (TitleInput input) =>
{
    if (string.IsNullOrWhiteSpace(input.Title))
    {
        return Results.ValidationProblem(new Dictionary<string, string[]>
        {
            ["title"] = new[] { "タイトルを入力してください。" }
        });
    }
    string title = input.Title.Trim();
    if (title.Length > 100)
    {
        return Results.ValidationProblem(new Dictionary<string, string[]>
        {
            ["title"] = new[] { "タイトルは100以内で入力してください。" }
        });
    }
    return Results.Ok(new { title });
});

app.Run();

public sealed class TitleInput
{
    public string? Title { get; set; }
}
