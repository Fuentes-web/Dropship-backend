from fastapi import FastAPI, Depends, HTTPException, status                           
from fastapi.middleware.cors import CORSMiddleware                                    
from sqlalchemy.orm import Session                                                    
from sqlalchemy import text                                                           
from contextlib import asynccontextmanager                                            
from typing import List, Optional                                                     
from datetime import datetime, timezone                                               
                                                                                          
from app.database import engine, Base, get_db, SessionLocal                           
from app.models import Product                                                        
from app.schemas import ProductCreate, ProductResponse, HealthResponse                
from app.seed import seed_products                                                    
                                                                                          
# Ciclo de vida: al iniciar la app crea las tablas y siembra los datos                
@asynccontextmanager                                                                  
async def lifespan(app: FastAPI):                                                     
    try:                                                                              
        Base.metadata.create_all(bind=engine)                                         
        with SessionLocal() as db:                                                    
            seed_products(db)                                                         
    except Exception as e:                                                            
        print(f"⚠️ Advertencia de base de datos al iniciar: {e}")                     
    yield                                                                             
                                                                                          
app = FastAPI(                                                                        
    title="Dropshipping Store API",                                                   
    description="API de catálogo y productos para Manifest Supply Co.",               
    version="1.0.0",                                                                  
    lifespan=lifespan                                                                 
)                                                                                     
                                                                                          
# Permitir CORS para que tu frontend en HTML/JS pueda comunicarse con esta API        
app.add_middleware(                                                                   
    CORSMiddleware,                                                                   
    allow_origins=["*"],                                                              
    allow_credentials=True,                                                           
    allow_methods=["*"],                                                              
    allow_headers=["*"],                                                              
)                                                                                     
                                                                                          
@app.get("/", tags=["Root"])                                                          
def root():
    return {
        "message": "Bienvenido a la API de Dropshipping",
        "docs": "/docs",
        "health": "/health",
        "products": "/products"
    }
  
    # 1. Endpoint /health solicitado
@app.get("/health", response_model=HealthResponse, tags=["Health"])
def health_check(db: Session = Depends(get_db)):
    db_status = "connected"
    try:
    # Ejecuta una consulta ultrarrápida para verificar PostgreSQL
        db.execute(text("SELECT 1"))
    except Exception as e:
        db_status = f"disconnected: {str(e)}"
  
    return {
        "status": "healthy" if db_status == "connected" else "degraded",
        "database": db_status,
        "timestamp": datetime.now(timezone.utc)
    }
  
    # 2. Endpoint /products: listar todos o filtrar por categoría
@app.get("/products", response_model=List[ProductResponse], tags=["Products"])        
def get_products(category: Optional[str] = None, db: Session = Depends(get_db)):      
    query = db.query(Product)
    if category and category.lower() != "all":
        query = query.filter(Product.category == category.lower())
    return query.all()
  
    # Endpoint para obtener un producto individual
@app.get("/products/{product_id}", response_model=ProductResponse, tags=["Products"]) 
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Producto con id {product_id} no encontrado"
        )
    return product
  
    # Endpoint para crear un nuevo producto
@app.post("/products", response_model=ProductResponse, status_code=status.            
    HTTP_201_CREATED, tags=["Products"])
def create_product(product_data: ProductCreate, db: Session = Depends(get_db)):       
    new_product = Product(**product_data.model_dump())
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product