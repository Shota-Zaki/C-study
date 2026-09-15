using System.Text;
var message = new StringBuilder();
message.AppendLine("注文番号: A001");
message.AppendLine("商品: ノート");
message.Append("発送準備中");
Console.WriteLine(message.ToString());
