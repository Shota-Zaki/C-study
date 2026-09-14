var actions = new List<Action>();
for (int i = 0; i < 3; i++)
{
    int captured = i;
    actions.Add(() => Console.WriteLine(captured));
}
foreach (Action action in actions)
{
    action();
}
