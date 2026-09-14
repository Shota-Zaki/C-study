var child = new Child("Aoi");
Console.WriteLine(child.Name);

public class Parent
{
    public string Name { get; }
    public Parent(string name)
    {
        Name = name;
        Console.WriteLine("Parent本体");
    }
}
public class Child : Parent
{
    public Child(string name) : base(name)
    {
        Console.WriteLine("Child本体");
    }
}
