int[] values = { 1, 2 };
Change(values);
Console.WriteLine(string.Join(",", values));

static void Change(int[] data)
{
    data[0] = 9;
    data = new[] { 7, 8 };
    Console.WriteLine(string.Join(",", data));
}
