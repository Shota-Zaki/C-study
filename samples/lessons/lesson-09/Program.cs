var learner = new Learner("ざき");
Console.WriteLine(learner.Introduce());

public class Learner
{
    public string Name { get; }

    public Learner(string name)
    {
        if (string.IsNullOrWhiteSpace(name))
            throw new ArgumentException("名前は必須です", nameof(name));
        Name = name.Trim();
    }

    public string Introduce() => $"{Name}です。C#を学習中です。";
}
