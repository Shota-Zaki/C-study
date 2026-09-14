using System.Net;
using System.Net.Http.Json;
using System.Text;

using var client = new HttpClient(new DemoHandler());
using HttpResponseMessage response = await client.GetAsync("https://example.invalid/items/3");
Console.WriteLine((int)response.StatusCode);
response.EnsureSuccessStatusCode();
Item? item = await response.Content.ReadFromJsonAsync<Item>();
Console.WriteLine(item?.Name ?? "データなし");

public record Item(int Id, string Name);

public sealed class DemoHandler : HttpMessageHandler
{
    protected override Task<HttpResponseMessage> SendAsync(
        HttpRequestMessage request, CancellationToken cancellationToken)
    {
        Console.WriteLine($"要求:{request.Method} {request.RequestUri?.AbsolutePath}");
        var response = new HttpResponseMessage(HttpStatusCode.OK)
        {
            Content = new StringContent("{\"id\":3,\"name\":\"Note\"}", Encoding.UTF8, "application/json")
        };
        return Task.FromResult(response);
    }
}
