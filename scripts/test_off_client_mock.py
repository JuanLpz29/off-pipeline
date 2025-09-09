from off_client.client import OFFClient
import json

# Datos simulados para prueba sin internet
mock_products = [
    {
        "code": "8414533104579",
        "product_name": "Granola con frutos secos",
        "ingredients_text": "avena, miel, almendras, pasas",
        "nutriments": {"energy": 450}
    },
    {
        "code": "7613036734219",
        "product_name": "Granola artesanal",
        "ingredients_text": "copos de avena, azúcar de coco, nueces",
        "nutriments": {"energy": 420}
    }
]

class OFFClientMock(OFFClient):
    def search_products(self, query: str, page_size: int = 20):
        """Versión simulada para pruebas sin internet"""
        print(f"🧪 Simulando búsqueda para: '{query}'")
        return mock_products[:page_size]

# Prueba con datos simulados
print("=== Prueba con datos simulados ===")
client_mock = OFFClientMock()
products = client_mock.search_products("granola", page_size=5)

print("Productos encontrados:")
for p in products:
    name = p.get("product_name", "<sin nombre>")
    code = p.get("code", "<sin código>")
    print(f" - {name} (code: {code})")
