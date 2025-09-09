# scripts/test_insert.py
import os

from dotenv import load_dotenv
from storage.postgres import PostgresStorage

load_dotenv()  # asegúrate de cargar .env

storage = PostgresStorage()

sample = {
    "code": "6294003539054",
    "name": "Kitkat",
    "ingredients": "chocolate, leche, azúcar, mantequilla de cacao",
    "calories": 535.0
}

storage.upsert_product(sample)
print("Producto insertado/actualizado:", sample["code"])
