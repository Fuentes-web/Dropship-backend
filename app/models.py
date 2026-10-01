from sqlalchemy import Column, Integer, String, Float, Boolean, Text, DateTime, func  
from app.database import Base                                                         
                                                                                          
class Product(Base):                                                                  
    __tablename__ = "products"                                                        
                                                                                          
    id = Column(Integer, primary_key=True, index=True)                                
    name = Column(String(200), nullable=False, index=True)                            
    description = Column(Text, nullable=True)                                         
    price = Column(Float, nullable=False)                                             
    original_price = Column(Float, nullable=True)                                     
    category = Column(String(50), nullable=False, index=True)                         
    rating = Column(Float, default=5.0)                                               
    tag = Column(String(50), nullable=True)                                           
    in_stock = Column(Boolean, default=True)                                          
    created_at = Column(DateTime(timezone=True), server_default=func.now())