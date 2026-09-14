Notice notice = new EmailNotice();
Console.WriteLine(notice.Send());

public class Notice
{
    public virtual string Send() => "通常の通知";
}
public class EmailNotice : Notice
{
    public override string Send() => "メール通知";
}
