from off_client.client import OFFClient
import json

client = OFFClient()
products = client.search_products("kitkat", page_size=5)

print("🔍 ANÁLISIS DETALLADO DE CAMPOS DE PRODUCTOS")
print("=" * 50)

for i, product in enumerate(products, 1):
    code = product.get("code", "sin código")
    print(f"\n📦 PRODUCTO {i} - Código: {code}")
    print("-" * 30)
    
    # Campos relacionados con nombres que podrían existir
    name_fields = [
        "product_name",
        "product_name_es",
        "product_name_en", 
        "abbreviated_product_name",
        "generic_name",
        "brands"
    ]
    
    print("🏷️  CAMPOS DE NOMBRE:")
    for field in name_fields:
        value = product.get(field, None)
        if value:
            print(f"   ✅ {field}: '{value}'")
        else:
            print(f"   ❌ {field}: None/Empty")
    
    # Si no hay product_name, veamos qué otros campos tienen contenido
    if not product.get("product_name"):
        print("\n🔍 OTROS CAMPOS DISPONIBLES (primeros 10):")
        available_fields = [(k, v) for k, v in product.items() if v and len(str(v)) < 100][:10]
        for key, value in available_fields:
            print(f"   • {key}: {value}")