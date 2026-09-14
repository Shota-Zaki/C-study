int score = 75;
string label = score switch
{
    < 0 or > 100 => "範囲外",
    >= 80 => "優秀",
    >= 60 => "合格",
    _ => "再挑戦"
};
Console.WriteLine(label);
