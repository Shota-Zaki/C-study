using System.Text.Json;

string root = Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.LocalApplicationData),
    "CSharpLearningLab");
string path = Path.Combine(root, "tasks.json");
string command = args.FirstOrDefault()?.ToLowerInvariant() ?? "help";
if (command == "where") { Console.WriteLine(path); return 0; }
if (command == "help")
{
    Console.WriteLine("コマンド: list / add \"タイトル\" / done ID / delete ID / where");
    return 0;
}
if (command is not ("list" or "add" or "done" or "delete"))
{
    Console.Error.WriteLine("不明なコマンドです。引数なしで使い方を表示します。");
    return 1;
}
try
{
    List<TaskItem> tasks = Load(path);
    switch (command)
    {
        case "list":
            if (args.Length != 1) throw new ArgumentException("listに追加の引数は不要です。");
            foreach (var item in tasks.OrderBy(x => x.CreatedAt))
                Console.WriteLine($"[{(item.Done ? "x" : " ")}] {item.Id} {item.Title}");
            Console.WriteLine($"{tasks.Count}件 / 完了{tasks.Count(x => x.Done)}件");
            return 0;
        case "add":
            if (args.Length != 2 || string.IsNullOrWhiteSpace(args[1]) || args[1].Trim().Length > 100)
                throw new ArgumentException("タイトルは1〜100文字。空白を含む場合は引用符で囲んでください。");
            if (tasks.Count >= 1000) throw new ArgumentException("タスクは1000件までです。");
            var added = new TaskItem(Guid.NewGuid(), args[1].Trim(), false, DateTimeOffset.UtcNow);
            tasks.Add(added);
            Save(path, tasks);
            Console.WriteLine($"追加: {added.Id} {added.Title}");
            return 0;
        default:
            if (args.Length != 2 || !Guid.TryParse(args[1], out Guid id))
                throw new ArgumentException("listに表示された有効なIDを指定してください。");
            int index = tasks.FindIndex(x => x.Id == id);
            if (index < 0) throw new ArgumentException("対象のタスクがありません。");
            if (command == "done") tasks[index] = tasks[index] with { Done = true };
            else tasks.RemoveAt(index);
            Save(path, tasks);
            Console.WriteLine(command == "done" ? "完了にしました。" : "削除しました。");
            return 0;
    }
}
catch (Exception ex) when (ex is IOException or UnauthorizedAccessException or JsonException or ArgumentException)
{
    Console.Error.WriteLine($"処理を中断しました: {ex.Message}");
    Console.Error.WriteLine($"保存先: {path}");
    return 1;
}

static List<TaskItem> Load(string path)
{
    string json;
    try { json = File.ReadAllText(path); }
    catch (FileNotFoundException) { return new List<TaskItem>(); }
    catch (DirectoryNotFoundException) { return new List<TaskItem>(); }
    if (json.Length > 2_000_000) throw new JsonException("保存データが大きすぎます。");
    var tasks = JsonSerializer.Deserialize<List<TaskItem>>(json)
        ?? throw new JsonException("保存データがnullです。初期化せず中断します。");
    if (tasks.Count > 1000 || tasks.Any(x => x is null || x.Id == Guid.Empty ||
        string.IsNullOrWhiteSpace(x.Title) || x.Title.Length > 100 || x.CreatedAt == default) ||
        tasks.Select(x => x.Id).Distinct().Count() != tasks.Count)
        throw new JsonException("保存データの内容に不正があります。初期化せず中断します。");
    return tasks;
}
static void Save(string path, List<TaskItem> tasks)
{
    Directory.CreateDirectory(Path.GetDirectoryName(path)!);
    string temporary = path + "." + Guid.NewGuid().ToString("N") + ".tmp";
    try
    {
        File.WriteAllText(temporary, JsonSerializer.Serialize(tasks,
            new JsonSerializerOptions { WriteIndented = true }));
        // 同一ディレクトリの一時ファイルから置き換える。複数プロセスの排他制御ではない。
        File.Move(temporary, path, overwrite: true);
    }
    finally
    {
        if (File.Exists(temporary)) File.Delete(temporary);
    }
}
public record TaskItem(Guid Id, string Title, bool Done, DateTimeOffset CreatedAt);

