var person = new Person();
person.Name = "  Aoi  ";
Console.WriteLine(person.Name);

public class Person
{
    private string _name = "未設定";

    public string Name
    {
        get { return _name; }
        set
        {
            if (string.IsNullOrWhiteSpace(value))
                throw new ArgumentException("名前が必要です");
            _name = value.Trim();
        }
    }
}
