string? name = null;
int? length = name?.Length;
int displayLength = length ?? 0;
string displayName = name ?? "未登録";
Console.WriteLine(length.HasValue);
Console.WriteLine(displayLength);
Console.WriteLine(displayName);
