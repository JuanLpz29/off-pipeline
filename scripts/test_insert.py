# scripts/test_insert.py
import os

from dotenv import load_dotenv
from storage.postgres import PostgresStorage

load_dotenv()  # asegúrate de cargar .env

storage = PostgresStorage()

sample = {
    "code": "000000001",
    "name": "Granola Tutorial",
    "ingredients": "avena, nueces, pasas",
    "calories": 350.0
}

storage.upsert_product(sample)
print("Producto insertado/actualizado:", sample["code"])
