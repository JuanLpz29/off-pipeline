import os
from dotenv import load_dotenv
import openfoodfacts
import requests

load_dotenv()  # carga las variables de .env

class OFFClient:
    def __init__(self):
        user_agent = os.getenv("OFF_USER_AGENT")
        if not user_agent:
            raise RuntimeError("OFF_USER_AGENT no está definido en .env")
        self.api = openfoodfacts.API(user_agent=user_agent)

    def search_products(self, query: str, page_size: int = 20):
        """Busca productos que coincidan con `query` en OFF."""
        try:
            result = self.api.product.text_search(query)
            products = result.get("products", [])[:page_size]
            return products
        except requests.exceptions.ConnectionError:
            print("❌ Error: No se pudo conectar a OpenFoodFacts. Verifica tu conexión a internet.")
            return []
        except Exception as e:
            print(f"❌ Error inesperado: {str(e)}")
            return []
