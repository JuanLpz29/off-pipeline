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

    def get_product_name(self, product: dict) -> str:
        """
        Extrae el nombre del producto usando múltiples campos de respaldo.
        
        Orden de prioridad:
        1. product_name - Nombre principal
        2. product_name_es - Nombre en español
        3. product_name_en - Nombre en inglés  
        4. abbreviated_product_name - Nombre abreviado
        5. generic_name - Nombre genérico (descripción)
        6. brands - Marcas como nombre de respaldo
        """
        name_fields = [
            "product_name",
            "product_name_es", 
            "product_name_en",
            "abbreviated_product_name",
            "generic_name"
        ]
        
        # Buscar primer campo con contenido válido
        for field in name_fields:
            name = product.get(field, "").strip()
            if name:
                return name
        
        # Si no hay nombre, usar marca como respaldo
        brands = product.get("brands", "").strip()
        if brands:
            # Tomar solo la primera marca si hay varias
            first_brand = brands.split(",")[0].strip()
            return f"{first_brand} (marca)"
        
        return "<sin nombre>"