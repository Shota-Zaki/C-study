var person = new Person();
Console.WriteLine(person.Name);
public class Person
{
    private string _name = "Aoi";
    public string Name => _name;
}
