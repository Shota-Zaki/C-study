using InventoryProduct = Inventory.Product;
using OrderProduct = Orders.Product;

Console.WriteLine(InventoryProduct.Label());
Console.WriteLine(OrderProduct.Label());

namespace Inventory
{
    public static class Product
    {
        public static string Label() => "在庫の商品";
    }
}

namespace Orders
{
    public static class Product
    {
        public static string Label() => "注文の商品";
    }
}
