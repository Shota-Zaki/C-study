var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();
var store = new TodoStore();

app.MapPost("/todos", (CreateTodo input) =>
{
    if (string.IsNullOrWhiteSpace(input.Title))
        return Results.BadRequest(new { error = "タイトルは必須です" });
    string title = input.Title.Trim();
    if (title.Length > 100)
        return Results.BadRequest(new { error = "タイトルが長すぎます" });
    Todo item = store.Add(title);
    return Results.Created($"/todos/{item.Id}", item);
});

app.MapGet("/todos/{id:int}", (int id) =>
{
    Todo? item = store.Find(id);
    return item is null ? Results.NotFound() : Results.Ok(item);
});

app.MapDelete("/todos/{id:int}", (int id) =>
    store.Remove(id) ? Results.NoContent() : Results.NotFound());

app.Run();

public record CreateTodo(string? Title);
public record Todo(int Id, string Title, bool Done);

public sealed class TodoStore
{
    private readonly object _gate = new();
    private readonly Dictionary<int, Todo> _items = new();
    private int _nextId;

    public Todo Add(string title)
    {
        lock (_gate)
        {
            int id = checked(_nextId + 1);
            var item = new Todo(id, title, false);
            _items.Add(id, item);
            _nextId = id;
            return item;
        }
    }
    public Todo? Find(int id)
    {
        lock (_gate)
        {
            return _items.TryGetValue(id, out Todo? item) ? item : null;
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
