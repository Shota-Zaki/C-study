AssertEqual(false, IsPassed(59), "59点");
AssertEqual(true, IsPassed(60), "60点");
AssertEqual(true, IsPassed(61), "61点");
Console.WriteLine("3件の検証に成功");

static bool IsPassed(int score) => score >= 60;
static void AssertEqual<T>(T expected, T actual, string caseName)
{
    if (!EqualityComparer<T>.Default.Equals(expected, actual))
        throw new InvalidOperationException($"{caseName}: 期待={expected}, 実際={actual}");
}
