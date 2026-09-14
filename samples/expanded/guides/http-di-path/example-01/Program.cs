var input = new CreateInput("  学習  ");
string? title = input.Title?.Trim();
if (string.IsNullOrWhiteSpace(title))
{
    Console.WriteLine("入力不正");
    return;
}
var saved = new Todo(1, title, false);
Console.WriteLine($"{saved.Id}:{saved.Title}:{saved.Done}");

record CreateInput(string? Title);
record Todo(int Id, string Title, bool Done);
