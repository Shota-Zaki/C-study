var builder = WebApplication.CreateBuilder(args);
builder.Services.AddSingleton<TaskStore>();
builder.Services.AddProblemDetails();
var app = builder.Build();
app.UseExceptionHandler();
app.MapGet("/health", () => Results.Ok(new { status = "ok" }));
app.MapGet("/tasks", (TaskStore store) => Results.Ok(store.All()));
app.MapGet("/tasks/{id:int}", GetTask);
app.MapPost("/tasks", CreateTask);
app.MapPut("/tasks/{id:int}/complete", CompleteTask);
app.MapDelete("/tasks/{id:int}", DeleteTask);
app.Run("http://127.0.0.1:5080");

static IResult GetTask(int id, TaskStore store)
{
    var task = store.Find(id);
    return task is null ? Results.NotFound() : Results.Ok(task);
}
static IResult CreateTask(CreateTaskRequest input, TaskStore store)
{
    if (string.IsNullOrWhiteSpace(input.Title) || input.Title.Trim().Length > 100)
        return Results.BadRequest(new { error = "タイトルは1〜100文字です。" });
    var task = store.Add(input.Title.Trim());
    return task is null
        ? Results.Conflict(new { error = "登録できるタスク数の上限に達しました。" })
        : Results.Created($"/tasks/{task.Id}", task);
}
static IResult CompleteTask(int id, TaskStore store)
{
    var task = store.Complete(id);
    return task is null ? Results.NotFound() : Results.Ok(task);
}
static IResult DeleteTask(int id, TaskStore store)
    => store.Delete(id) ? Results.NoContent() : Results.NotFound();

public record CreateTaskRequest(string? Title);
public record TaskItem(int Id, string Title, bool Done);
public sealed class TaskStore
{
    private readonly object gate = new();
    private readonly Dictionary<int, TaskItem> tasks = new();
    private int nextId;
    public TaskItem[] All()
    {
        lock (gate) return tasks.Values.OrderBy(x => x.Id).ToArray();
    }
    public TaskItem? Find(int id)
    {
        lock (gate) return tasks.GetValueOrDefault(id);
    }
    public TaskItem? Add(string title)
    {
        lock (gate)
        {
            if (tasks.Count >= 1000 || nextId == int.MaxValue) return null;
            var task = new TaskItem(++nextId, title, false);
            tasks.Add(task.Id, task);
            return task;
        }
    }
    public TaskItem? Complete(int id)
    {
        lock (gate)
        {
            if (!tasks.TryGetValue(id, out var task)) return null;
            return tasks[id] = task with { Done = true };
        }
    }
    public bool Delete(int id)
    {
        lock (gate) return tasks.Remove(id);
    }
}

