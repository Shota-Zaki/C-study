var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();
app.MapGet("/lessons/{id:int}", GetLesson);
app.Run("http://127.0.0.1:5080");

static IResult GetLesson(int id)
{
    if (id is < 1 or > 32)
        return Results.NotFound(new { error = "レッスンがありません" });
    return Results.Ok(new { id, title = $"Lesson {id}" });
}
