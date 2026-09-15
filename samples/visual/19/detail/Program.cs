var items = new[] { (Category: "本", Amount: 1000), (Category: "文具", Amount: 300), (Category: "本", Amount: 500) };
foreach (var group in items.GroupBy(x => x.Category).OrderBy(g => g.Key, StringComparer.Ordinal))
    Console.WriteLine($"{group.Key}: {group.Sum(x => x.Amount)}円");
