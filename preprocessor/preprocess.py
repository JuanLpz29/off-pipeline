# preprocessor/preprocess.py

import pandas as pd

def normalize_product(raw: dict, client) -> dict:
    """
    Toma un producto crudo de OFF y devuelve
    un dict con campos estandarizados.
    Usa el método get_product_name del cliente para extraer nombres robustamente.
    """
    return {
        "code": raw.get("code"),
        "name": client.get_product_name(raw).lower().strip(),
        "brands": raw.get("brands", "").strip(),
        "ingredients": raw.get("ingredients_text", "").strip(),
        "calories": raw.get("nutriments", {}).get("energy-kcal_100g"),
    }

def to_dataframe(products: list[dict], client) -> pd.DataFrame:
    """
    Convierte una lista de dicts normalizados
    en un DataFrame y descarta registros inválidos.
    """
    df = pd.DataFrame([normalize_product(p, client) for p in products])
    return df.dropna(subset=["code", "name"])
