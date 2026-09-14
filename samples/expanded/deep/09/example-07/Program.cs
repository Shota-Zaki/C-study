var person = new Person("Aoi");
Console.WriteLine(person.Name);
public class Person
{
    private string name;
    public string Name => name;
    public Person(string name)
    {
        this.name = name;
    }
}
