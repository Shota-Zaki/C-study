bool saved = false;
try
{
    throw new IOException("保存先へ書き込めません");
}
catch (IOException)
{
    Console.WriteLine("保存に失敗しました。入力は保持します。");
}
Console.WriteLine(saved);
