string input = " 42 ";
if (int.TryParse(input, out int value))
    Console.WriteLine(value * 2);
else
    Console.WriteLine("変換できません");
