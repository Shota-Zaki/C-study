using System.Net;
using System.Net.Http.Json;

using var client = new HttpClient(new DemoHandler());
using var response = await client.GetAsync("https://example.invalid/score");
response.EnsureSuccessStatusCode();
var score = await response.Content.ReadFromJsonAsync<Score>()
    ?? throw new InvalidOperationException("応答が空です");
Console.WriteLine(score.Value);

public record Score(int Value);
public class DemoHandler : HttpMessageHandler
{
    protected override Task<HttpResponseMessage> SendAsync(HttpRequestMessage request, CancellationToken token)
    {
        token.ThrowIfCancellationRequested();
        return Task.FromResult(new HttpResponseMessage(HttpStatusCode.OK)
        {
            Content = JsonContent.Create(new Score(80))
        });
    }
}
