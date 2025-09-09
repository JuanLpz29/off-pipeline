import os
from dotenv import load_dotenv
from off_client.client import OFFClient
from preprocessor.preprocess import to_dataframe

load_dotenv()  

client = OFFClient()
raws = client.search_products("kitkat", page_size=5)
df = to_dataframe(raws, client)  # Pasar cliente para usar get_product_name()

# Guardar el DataFrame en un archivo txt
ruta_salida = "resultado_dataframe.txt"
with open(ruta_salida, "w", encoding="utf-8") as f:
    f.write("DataFrame resultante:\n")
    f.write(df.to_string(index=False))

print(f"El DataFrame se ha guardado en '{ruta_salida}'")
