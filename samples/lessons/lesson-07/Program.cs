Console.WriteLine(Add(5));
Console.WriteLine(Add(value: 5, step: 3));
int count = 1;
Increment(ref count);
Console.WriteLine(count);

static int Add(int value, int step = 1) => value + step;
static void Increment(ref int value) => value++;
