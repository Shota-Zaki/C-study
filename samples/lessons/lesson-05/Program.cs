int score = 82;
string result = score switch
{
    < 0 or > 100 => "範囲外",
    >= 80 => "よくできました",
    >= 60 => "合格",
    _ => "再学習"
};
Console.WriteLine(result);
