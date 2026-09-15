var store = new Dictionary<int, string>();
store.Add(1, "Review");
Console.WriteLine(store.ContainsKey(1));
Console.WriteLine(store.Remove(1));
Console.WriteLine(store.ContainsKey(1));
Console.WriteLine(store.Remove(1));
