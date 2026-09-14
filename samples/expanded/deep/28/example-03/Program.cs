using System.Net;
using System.Net.Http.Json;
using System.Text;

using var response = new HttpResponseMessage(HttpStatusCode.NotFound)
{
    Content = new StringContent("not found", Encoding.UTF8, "text/plain")
};
if (response.StatusCode == HttpStatusCode.NotFound)
{
    Console.WriteLine("対象がありません");
}
else
{
    response.EnsureSuccessStatusCode();
    Item? item = await response.Content.ReadFromJsonAsync<Item>();
    Console.WriteLine(item?.Name ?? "データなし");
}

public record Item(int Id, string Name);
