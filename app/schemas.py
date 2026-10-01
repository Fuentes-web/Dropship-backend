from pydantic import BaseModel, ConfigDict, Field, EmailStr
from typing import Optional, List, Any
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

# --- Esquemas para Órdenes y Pagos ---

class OrderItemCreate(BaseModel):
    product_id: int
    quantity: int = Field(gt=0, description="La cantidad debe ser mayor a 0")

class OrderItemDetail(BaseModel):
    product_id: int
    name: str
    price: float
    quantity: int
    subtotal: float

class OrderCreate(BaseModel):
    customer_name: str
    customer_email: str
    shipping_address: str
    items: List[OrderItemCreate] = Field(min_length=1, description="Debe incluir al menos un producto")

class OrderResponse(BaseModel):
    id: int
    order_number: str
    customer_name: str
    customer_email: str
    shipping_address: str
    items: List[Any]
    total_amount: float
    status: str
    payment_status: str
    payment_error_reason: Optional[str] = None
    transaction_id: Optional[str] = None
    created_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)

# --- Esquema para el endpoint /slow ---
class SlowResponse(BaseModel):
    status: str
    delay_seconds: float
    message: str
    timestamp: datetime