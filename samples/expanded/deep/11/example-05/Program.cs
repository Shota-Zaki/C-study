BaseLabel label = new DetailedLabel();
Console.WriteLine(label.GetLabel());
public class BaseLabel
{
    public virtual string GetLabel() => "基本";
}
public class DetailedLabel : BaseLabel
{
    public override string GetLabel() => "詳細";
}
