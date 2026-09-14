var person = new Person("Aoi");
Console.WriteLine($"[{person.Name}]");
public class Person
{
    private string name = "未設定";
    public string Name => name;
    public Person(string name)
    {
        name = name;
    }
}
