Task<int> first = Task.FromResult(10);
Task<int> second = Task.FromResult(20);
Task<int> completed = await Task.WhenAny(first, second);
int result = await completed;
Console.WriteLine(result is 10 or 20);
