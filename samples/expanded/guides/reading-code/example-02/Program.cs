Console.WriteLine("開始");
int answer = Add(2, 3);
Console.WriteLine(answer);
Console.WriteLine("終了");

static int Add(int left, int right)
{
    Console.WriteLine("計算中");
    return left + right;
}
