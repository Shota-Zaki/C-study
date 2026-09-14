var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

app.MapGet("/hello", () => new { message = "Hello CSharp" });
app.MapGet("/lessons/{id:int}", (int id) => new { id, title = $"Lesson {id}" });

app.Run("http://127.0.0.1:5080");
