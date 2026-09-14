var original = new Group { Name = "元", Scores = new[] { 10, 20 } };
Group copied = original;
copied.Name = "コピー";
copied.Scores[0] = 99;
Console.WriteLine(original.Name);
Console.WriteLine(original.Scores[0]);

public struct Group
{
    public string Name;
    public int[] Scores;
}
