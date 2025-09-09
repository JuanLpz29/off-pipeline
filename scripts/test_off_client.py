from off_client.client import OFFClient

client = OFFClient()
products = client.search_products("pie de limón", page_size=5)

print("Productos encontrados:")
for p in products:
    name = p.get("product_name", "<sin nombre>")
    code = p.get("code", "<sin código>")
    print(f" - {name} (code: {code})")
