import os                                                                             
from sqlalchemy import create_engine                                                  
from sqlalchemy.orm import declarative_base, sessionmaker                             
                                                                                          
# 1. Leemos la URL de la base de datos desde las variables de entorno                 
# Por defecto se conecta a PostgreSQL en localhost:5432                               
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg2://postgres:postgres@localhost:5432/dropship_db"
)

# Si viene como postgresql:// lo adaptamos para el driver psycopg2 instalado
if DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+psycopg2://", 1)

# 2. Creamos el motor de SQLAlchemy
engine = create_engine(DATABASE_URL)                                                  
                                                                                          
# 3. Fábrica de sesiones para interactuar con la BD                                   
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)           
                                                                                          
# 4. Clase base para nuestros modelos ORM                                             
Base = declarative_base()                                                             
                                                                                          
# 5. Inyección de dependencias: abre una sesión y la cierra al terminar la petición   
def get_db():                                                                         
    db = SessionLocal()                                                               
    try:                                                                              
        yield db                                                                      
    finally:                                                                          
        db.close() 