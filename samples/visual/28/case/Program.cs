using System.Net;
using System.Net.Http;
using var response = new HttpResponseMessage(HttpStatusCode.NotFound);
if (response.IsSuccessStatusCode)
    Console.WriteLine("取得成功");
else if (response.StatusCode == HttpStatusCode.NotFound)
    Console.WriteLine("対象が見つかりません");
else
    Console.WriteLine($"HTTPエラー: {(int)response.StatusCode}");
