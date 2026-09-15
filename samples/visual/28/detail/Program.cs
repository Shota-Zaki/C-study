using System.Net;
using System.Net.Http;
foreach (int code in new[] { 200, 201, 204, 400, 404, 500 })
{
    using var response = new HttpResponseMessage((HttpStatusCode)code);
    Console.WriteLine($"{code}: {response.IsSuccessStatusCode}");
}
