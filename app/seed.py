from sqlalchemy.orm import Session                                                    
from app.models import Product                                                        
                                                                                          
SAMPLE_PRODUCTS = [                                                                   
    {                                                                                 
        "name": "Aether Studio Wireless Headphones",                                  
        "description": "Hybrid ANC, 60-hour battery, machined aluminium yokes.",      
        "price": 129.0,                                                               
        "original_price": 189.0,                                                      
        "category": "audio",                                                          
        "rating": 4.9,                                                                
        "tag": "Sale",                                                                
        "in_stock": True                                                              
    },                                                                                
    {                                                                                 
        "name": "Halcyon Ceramic Table Lamp",                                         
        "description": "Warm-dimming LED, slip-cast stoneware, brass dimmer knob.",   
        "price": 84.0,                                                                
        "original_price": 110.0,                                                      
        "category": "home",                            
        "rating": 4.8,                                                                
        "tag": "Bestseller",                                                          
        "in_stock": True                                                              
    },                                                                                
    {                                                                                 
        "name": "Vantage Field Chronograph",                                          
        "description": "Seiko VK64 meca-quartz, sapphire crystal, 100m water resistance.",                                                                           
        "price": 195.0,                                                               
        "original_price": 240.0,                                                      
        "category": "wearables",                                                      
        "rating": 5.0,                                                                
        "tag": "New",                                                                 
        "in_stock": True                                                              
    },                                                                                
    {                                                                                 
        "name": "Nomad Titanium Mechanical Pencil",                                   
        "description": "Grade 5 titanium body, 0.5mm Schmidt mechanism, knurled grip.",
        "price": 46.0,                                                                
        "original_price": 55.0,                                                       
        "category": "carry",                                                          
        "rating": 4.9,                                                                
        "tag": "Staff Pick",                                                          
        "in_stock": True                                                              
    },                                                                                
    {                                                                                 
        "name": "Aerofoil Packable Windbreaker",                                      
        "description": "Ultralight ripstop nylon, DWR finish, packs into its own pocket.",                                                                               
        "price": 78.0,                                                                
        "original_price": 95.0,                                                       
        "category": "travel",                                                         
        "rating": 4.7,                                                                
        "tag": None,                                                                  
        "in_stock": True                                                              
    }                                                                                 
]
                                                                                          
def seed_products(db: Session):                                                       
    # Solo insertamos si la tabla de productos está vacía                             
    if db.query(Product).first() is None:                                             
        for item in SAMPLE_PRODUCTS:                                                  
            product = Product(**item)                                                 
            db.add(product)                                                           
        db.commit()