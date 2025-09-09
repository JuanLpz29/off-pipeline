from off_client.client import OFFClient

client = OFFClient()
products = client.search_products("kitkat", page_size=5)

print("Productos encontrados:")
for p in products:
    name = client.get_product_name(p)  # Usa el nuevo método mejorado
    code = p.get("code", "<sin código>")
    brand = p.get("brands", "<sin marca>")
    print(f" - {name} (code: {code}, marca: {brand})")
