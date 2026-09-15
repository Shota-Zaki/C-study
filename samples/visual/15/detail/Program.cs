var participants = new HashSet<string>(StringComparer.OrdinalIgnoreCase);
Console.WriteLine(participants.Add("Aoi"));
Console.WriteLine(participants.Add("AOI"));
Console.WriteLine(participants.Count);
