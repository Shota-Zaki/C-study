using Microsoft.Extensions.Options;

var builder = WebApplication.CreateBuilder(args);
builder.Services.AddOptions<StudyOptions>()
    .Bind(builder.Configuration.GetSection("Study"))
    .Validate(options => !string.IsNullOrWhiteSpace(options.Title), "Titleは必須です")
    .Validate(options => options.MaxItems is >= 1 and <= 1000, "MaxItemsは1〜1000です")
    .ValidateOnStart();
var app = builder.Build();

app.MapGet("/settings-summary", (IOptions<StudyOptions> options) =>
    Results.Ok(new { title = options.Value.Title, maxItems = options.Value.MaxItems }));

app.Run();

public sealed class StudyOptions
{
    public string Title { get; set; } = "C# Learning Lab";
    public int MaxItems { get; set; } = 100;
}
