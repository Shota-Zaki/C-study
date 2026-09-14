using System;

internal class Program
{
    private static void Main()
    {
        Console.WriteLine("入口");
        PrintMessage();
        Console.WriteLine("終了");
    }

    private static void PrintMessage()
    {
        Console.WriteLine("呼び出された処理");
    }
}
