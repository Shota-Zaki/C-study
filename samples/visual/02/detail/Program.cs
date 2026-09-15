using TextBuffer = System.Text.StringBuilder;
var a = new System.Text.StringBuilder("A");
var b = new TextBuffer("B");
Console.WriteLine(a.GetType() == b.GetType());
Console.WriteLine(a.ToString() + b.ToString());
