import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base, Product
from sqlalchemy import text

class PostgresStorage:
    def __init__(self):
        # Carga la URL desde la variable de entorno
        url = os.getenv("POSTGRES_URL")
        self.engine = create_engine(url)
        # Crea las tablas si no existen
        Base.metadata.create_all(self.engine)
        # Prepara factory de sesiones
        self.Session = sessionmaker(bind=self.engine)

    def upsert_product(self, product_data: dict):
        session = self.Session()
        # merge inserta o actualiza según PK
        obj = Product(**product_data)
        session.merge(obj)
        session.commit()
        session.close()
