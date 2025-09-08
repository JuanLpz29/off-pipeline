from sqlalchemy import Column, String, Float
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

class Product(Base):
    __tablename__ = "products"
    code = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    ingredients = Column(String)
    calories = Column(Float)
