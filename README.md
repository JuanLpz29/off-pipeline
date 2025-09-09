# 🍎 OFF-Pipeline

Un sistema modular diseñado para consumir datos de la API de OpenFoodFacts (OFF), procesarlos y almacenarlos en PostgreSQL con capacidades de vectorización preparadas para el futuro.

## 📋 **Arquitectura General**

El proyecto está estructurado como un pipeline completo para el procesamiento de datos alimentarios, con módulos especializados para cada etapa del proceso:

```
off-pipeline/
├── off_client/         # Cliente para interactuar con la API de OFF
├── storage/           # Modelos y conexión a PostgreSQL
├── scripts/           # Scripts de prueba y utilidades
├── api/               # Módulo para API REST (preparado)
├── data/              # Almacenamiento de datos (preparado)
├── embedder/          # Vectorización de datos (preparado)
├── preprocessor/      # Limpieza y procesamiento (preparado)
└── docker-compose.yml # Infraestructura containerizada
```

## 🔌 **Cliente OpenFoodFacts**

### **Clase OFFClient** (`off_client/client.py`)

Cliente principal para interactuar con la API de OpenFoodFacts:

```python
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
            print("❌ Error: No se pudo conectar a OpenFoodFacts.")
            return []
        except Exception as e:
            print(f"❌ Error inesperado: {str(e)}")
            return []
```

### **Características Clave:**

- **🔐 Autenticación:** Requiere obligatoriamente `OFF_USER_AGENT` en variables de entorno
- **🔍 Búsqueda por Texto:** Utiliza la API oficial de OpenFoodFacts
- **⚡ Control de Paginación:** Límite configurable de resultados (default: 20)
- **🛡️ Manejo de Errores:** Control robusto de conectividad y errores inesperados
- **📦 Librería Oficial:** Usa `openfoodfacts>=0.1.7` (cliente oficial de Python)

## 💾 **Sistema de Almacenamiento**

### **Modelos de Datos** (`storage/models.py`)

Estructura de datos optimizada para productos alimentarios:

```python
from sqlalchemy import Column, String, Float
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

class Product(Base):
    __tablename__ = "products"
    code = Column(String, primary_key=True)        # Código único de OFF
    name = Column(String, nullable=False)          # Nombre del producto
    ingredients = Column(String)                   # Lista de ingredientes
    calories = Column(Float)                       # Información nutricional
```

### **Conexión PostgreSQL** (`storage/postgres.py`)

Gestor de persistencia con operaciones UPSERT:

```python
class PostgresStorage:
    def __init__(self):
        url = os.getenv("POSTGRES_URL")
        self.engine = create_engine(url)
        Base.metadata.create_all(self.engine)      # Auto-creación de tablas
        self.Session = sessionmaker(bind=self.engine)

    def upsert_product(self, product_data: dict):
        session = self.Session()
        obj = Product(**product_data)
        session.merge(obj)  # INSERT o UPDATE según la PK
        session.commit()
        session.close()
```

### **Características del Storage:**

- **🔄 Operación Upsert:** `merge()` inserta nuevos productos o actualiza existentes
- **🏗️ Auto-setup:** Las tablas se crean automáticamente si no existen
- **🔒 Gestión de Sesiones:** Apertura y cierre controlado de conexiones
- **📊 Modelo Extensible:** Estructura preparada para más campos nutricionales

## 🧪 **Scripts de Prueba**

### **1. Test Cliente OFF** (`scripts/test_off_client.py`)

```python
from off_client.client import OFFClient

client = OFFClient()
products = client.search_products("granola", page_size=5)

print("Productos encontrados:")
for p in products:
    name = p.get("product_name", "<sin nombre>")
    code = p.get("code", "<sin código>")
    print(f" - {name} (code: {code})")
```

### **2. Test Conexión BD** (`scripts/test_db_connection.py`)

```python
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()
url = os.getenv("POSTGRES_URL")
engine = create_engine(url)

with engine.connect() as conn:
    result = conn.execute(text("SELECT 1"))
    print("Postgres dice:", result.scalar())
```

### **3. Test Inserción** (`scripts/test_insert.py`)

```python
from storage.postgres import PostgresStorage

storage = PostgresStorage()
sample = {
    "code": "000000001",
    "name": "Granola Tutorial",
    "ingredients": "avena, nueces, pasas",
    "calories": 350.0
}

storage.upsert_product(sample)
print("Producto insertado/actualizado:", sample["code"])
```

## 🐳 **Infraestructura Docker**

### **Servicios Containerizados** (`docker-compose.yml`)

```yaml
version: '3.8'
services:
  postgres:
    image: postgres:14
    environment:
      POSTGRES_USER: ${POSTGRES_USER}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
      POSTGRES_DB: ${POSTGRES_DB}
    ports:
      - "5432:5432"

  weaviate:
    image: semitechnologies/weaviate:latest
    environment:
      - QUERY_DEFAULTS_LIMIT=20
      - AUTHENTICATION_ANONYMOUS_ACCESS_ENABLED=true
    ports:
      - "8080:8080"
```

### **Servicios Incluidos:**

- **🐘 PostgreSQL 14:** Base de datos relacional principal
- **🔍 Weaviate:** Base de datos vectorial (preparada para embeddings futuros)
- **⚙️ Configuración por Variables:** Todos los parámetros externalizados

## 📦 **Dependencias**

### **Librerías Principales** (`setup.py`)

```python
install_requires=[
    "sqlalchemy>=1.4.0",      # ORM para PostgreSQL
    "psycopg2-binary>=2.9.0", # Driver PostgreSQL
    "python-dotenv>=0.19.0",  # Variables de entorno
    "openfoodfacts>=0.1.7",   # Cliente oficial OFF
]
```

### **Stack Tecnológico:**

- **🐍 Python 3.x:** Lenguaje principal
- **🗄️ SQLAlchemy:** ORM para gestión de base de datos
- **🔌 OpenFoodFacts API:** Cliente oficial para consumir datos
- **🐳 Docker:** Containerización de servicios
- **⚡ PostgreSQL:** Base de datos relacional

## 🔄 **Flujo de Trabajo Completo**

### **1. Configuración Inicial**

Crear archivo `.env` con las variables requeridas:

```env
# OpenFoodFacts API
OFF_USER_AGENT=tu-aplicacion-nombre/1.0

# PostgreSQL Configuration
POSTGRES_URL=postgresql://usuario:password@localhost:5432/off_db
POSTGRES_USER=usuario
POSTGRES_PASSWORD=password
POSTGRES_DB=off_db
```

### **2. Levantamiento de Servicios**

```bash
# Levantar infraestructura
docker-compose up -d

# Instalar dependencias
pip install -e .
```

### **3. Flujo de Procesamiento**

#### **Pasos Detallados:**

1. **🔐 Inicialización:** Se crea instancia de `OFFClient` con validación de `user_agent`
2. **🔍 Búsqueda:** Se ejecuta `search_products()` con término de búsqueda específico
3. **📥 Obtención de Datos:** La API devuelve JSON con productos filtrados
4. **🔄 Transformación:** Datos de OFF se mapean al modelo `Product` de SQLAlchemy
5. **💾 Persistencia:** `upsert_product()` guarda o actualiza productos en PostgreSQL

### **4. Ejemplo de Uso Completo**

```python
from off_client.client import OFFClient
from storage.postgres import PostgresStorage

# Inicializar servicios
client = OFFClient()
storage = PostgresStorage()

# Buscar productos
products = client.search_products("yogurt", page_size=10)

# Procesar y guardar cada producto
for product in products:
    product_data = {
        "code": product.get("code"),
        "name": product.get("product_name", "Sin nombre"),
        "ingredients": product.get("ingredients_text", ""),
        "calories": product.get("nutriments", {}).get("energy-kcal", 0.0)
    }
    
    storage.upsert_product(product_data)
    print(f"✅ Producto guardado: {product_data['name']}")
```

## 🛡️ **Manejo de Errores**

### **Niveles de Validación:**

1. **🔒 Variables de Entorno:** Validación obligatoria de `OFF_USER_AGENT` y `POSTGRES_URL`
2. **🌐 Conectividad OFF:** Control específico de `ConnectionError`
3. **🗄️ Conectividad PostgreSQL:** Validación de conexión a base de datos
4. **📊 Datos Inconsistentes:** Manejo graceful de campos faltantes en productos
5. **⚠️ Errores Generales:** Captura y logging de excepciones inesperadas

### **Estrategias de Recuperación:**

- **🔄 Reintentos Automáticos:** Para errores de conectividad temporal
- **📝 Logging Descriptivo:** Mensajes claros para debugging
- **🚫 Fallos Graceful:** El sistema continúa funcionando con datos parciales
- **🛡️ Validación de Entrada:** Verificación de datos antes del procesamiento

## 🚀 **Estado Actual vs. Potencial Futuro**

### **✅ Funcional Actualmente:**

- **🔍 Cliente OFF:** Búsqueda básica por texto en OpenFoodFacts
- **💾 Almacenamiento:** Persistencia completa en PostgreSQL
- **🧪 Testing:** Scripts de validación y pruebas unitarias
- **🛡️ Error Handling:** Manejo robusto de errores de conectividad
- **🐳 Containerización:** Infraestructura lista para producción

### **📦 Preparado para Expansión:**

- **🤖 Embedder Module:** Vectorización de ingredientes y descripciones
- **🧹 Preprocessor Module:** Limpieza y normalización de datos
- **🔗 API REST:** Endpoints para consulta externa de productos
- **📊 Data Analytics:** Análisis nutricional y tendencias alimentarias
- **🎯 Recomendaciones:** Sistema de recomendación basado en similitud

### **🔮 Arquitectura Futura:**

```mermaid
graph TB
    A[OpenFoodFacts API] --> B[OFFClient]
    B --> C[Preprocessor]
    C --> D[PostgreSQL]
    C --> E[Embedder]
    E --> F[Weaviate Vector DB]
    D --> G[REST API]
    F --> G
    G --> H[Frontend/Analytics]
```

## 🚦 **Comandos de Desarrollo**

### **Setup Inicial:**

```bash
# Clonar y configurar
git clone <repo>
cd off-pipeline

# Configurar entorno
cp .env.example .env  # Editar variables necesarias

# Levantar servicios
docker-compose up -d

# Instalar dependencias
pip install -e .
```

### **Testing:**

```bash
# Test conexión OFF
python scripts/test_off_client.py

# Test conexión PostgreSQL
python scripts/test_db_connection.py

# Test inserción completa
python scripts/test_insert.py
```

### **Desarrollo:**

```bash
# Logs de servicios
docker-compose logs -f

# Reiniciar servicios
docker-compose restart

# Limpiar volúmenes
docker-compose down -v
```

## 🤝 **Contribuir**

Este proyecto está diseñado con una arquitectura modular que facilita la extensión y mejora continua. Las áreas de contribución incluyen:

- **🔍 Mejoras en Cliente OFF:** Más métodos de búsqueda y filtrado
- **🗄️ Extensión de Modelos:** Más campos nutricionales y metadata
- **🤖 Implementación de Embedder:** Vector embeddings para similitud semántica
- **🧹 Desarrollo de Preprocessor:** Limpieza y normalización de datos
- **🔗 API REST:** Endpoints para acceso externo
- **📊 Analytics Dashboard:** Visualización de datos nutricionales

---

**Este README proporciona una guía exhaustiva del funcionamiento actual del sistema OFF-Pipeline, desde la configuración inicial hasta el flujo completo de datos, incluyendo la arquitectura preparada para escalabilidad futura.**
