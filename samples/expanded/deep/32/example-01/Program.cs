var builder = WebApplication.CreateBuilder(args);
builder.Services.AddProblemDetails();
builder.Services.AddSingleton<TodoStore>();
var app = builder.Build();
app.UseExceptionHandler();

app.MapGet("/todos", (TodoStore store) => Results.Ok(store.All()));

app.MapGet("/todos/{id:int}", (int id, TodoStore store) =>
{
    Todo? item = store.Find(id);
    return item is null ? Results.NotFound() : Results.Ok(item);
});

app.MapPost("/todos", (CreateTodo input, TodoStore store, ILogger<Program> logger) =>
{
    AddResult result = store.TryAdd(input.Title);
    if (result.Item is null)
    {
        return Results.ValidationProblem(new Dictionary<string, string[]>
        {
            ["title"] = new[] { result.Error ?? "タイトルを確認してください。" }
        });
    }
    logger.LogInformation("Todo {TodoId} created", result.Item.Id);
    return Results.Created($"/todos/{result.Item.Id}", result.Item);
});

app.MapPut("/todos/{id:int}/completion", (int id, CompletionInput input, TodoStore store) =>
{
    if (input.Done is not bool done)
        return Results.BadRequest(new { error = "doneを指定してください" });
    Todo? item = store.SetCompletion(id, done);
    return item is null ? Results.NotFound() : Results.Ok(item);
});

app.MapDelete("/todos/{id:int}", (int id, TodoStore store) =>
    store.Remove(id) ? Results.NoContent() : Results.NotFound());

app.Run();

public partial class Program { }
public record CreateTodo(string? Title);
public record CompletionInput(bool? Done);
public record Todo(int Id, string Title, bool Done);
public record AddResult(Todo? Item, string? Error);

public sealed class TodoStore
{
    private readonly object _gate = new();
    private readonly Dictionary<int, Todo> _items = new();
    private int _nextId;

    public AddResult TryAdd(string? rawTitle)
    {
        if (string.IsNullOrWhiteSpace(rawTitle))
            return new(null, "タイトルは必須です。");
        string title = rawTitle.Trim();
        if (title.Length > 100)
            return new(null, "タイトルの長さは100以内です。");
        lock (_gate)
        {
            int id = checked(_nextId + 1);
            var item = new Todo(id, title, false);
            _items.Add(id, item);
            _nextId = id;
            return new(item, null);
        }
    }
    public Todo[] All()
    {
        lock (_gate)
        {
            return _items.Values.OrderBy(item => item.Id).ToArray();
        }
    }
    public Todo? Find(int id)
    {
        lock (_gate)
        {
            return _items.TryGetValue(id, out Todo? item) ? item : null;
        }
    }
    public Todo? SetCompletion(int id, bool done)
    {
        lock (_gate)
        {
            if (!_items.TryGetValue(id, out Todo? item)) return null;
            Todo updated = item with { Done = done };
            _items[id] = updated;
            return updated;
        }
    }
    public bool Remove(int id)
    {
        lock (_gate)
        {
            return _items.Remove(id);
        }
    }
}
