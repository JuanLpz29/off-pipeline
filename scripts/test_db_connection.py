# scripts/test_db_connection.py
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

# 1) Indica dónde está tu .env (por defecto busca en la raíz del proyecto)
load_dotenv()  

# 2) Recupera la URL
url = os.getenv("POSTGRES_URL")
if url is None:
    raise RuntimeError("POSTGRES_URL no está definida en el entorno")

# 3) Conéctate
engine = create_engine(url)
with engine.connect() as conn:
    result = conn.execute(text("SELECT 1"))
    print("Postgres dice:", result.scalar())
