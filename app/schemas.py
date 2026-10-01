from pydantic import BaseModel, ConfigDict                                            
from typing import Optional                                                           
from datetime import datetime                                                         
                                                                                          
# Esquema base con campos comunes                                                     
class ProductBase(BaseModel):                                                         
    name: str                                                                         
    description: Optional[str] = None                                                 
    price: float                                                                      
    original_price: Optional[float] = None                                            
    category: str                                                                     
    rating: Optional[float] = 5.0                                                     
    tag: Optional[str] = None                                                         
    in_stock: Optional[bool] = True                                                   
                                                                                          
# Esquema para crear un nuevo producto (los datos que pedimos al cliente)             
class ProductCreate(ProductBase):                                                     
    pass                                                                              
                                                                                          
# Esquema para responder con un producto (incluye ID y fecha de creación generados por la BD)                                                                                  
class ProductResponse(ProductBase):                                                   
    id: int                                                                           
    created_at: Optional[datetime] = None                                             
                                                                                          
    model_config = ConfigDict(from_attributes=True)                                   
                                                                                          
# Esquema para el endpoint /health                                                    
class HealthResponse(BaseModel):                                                      
    status: str                                                                       
    database: str                                                                     
    timestamp: datetime