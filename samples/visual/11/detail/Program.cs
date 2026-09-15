BaseMessage message = new ShippingMessage();
Console.WriteLine(message.Build());
class BaseMessage
{
    public virtual string Build() => "注文を確認しました";
}
class ShippingMessage : BaseMessage
{
    public override string Build() => base.Build() + " / 発送待ち";
}
