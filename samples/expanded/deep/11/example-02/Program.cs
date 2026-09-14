BaseLabel asBase = new DetailedLabel();
DetailedLabel asDerived = new DetailedLabel();
Console.WriteLine(asBase.GetLabel());
Console.WriteLine(asDerived.GetLabel());

public class BaseLabel
{
    public string GetLabel() => "基本";
}
public class DetailedLabel : BaseLabel
{
    public new string GetLabel() => "詳細";
}
