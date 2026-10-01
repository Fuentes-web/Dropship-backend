from sqlalchemy import Column, Integer, String, Float, Boolean, Text, DateTime, JSON, func
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

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    order_number = Column(String(50), unique=True, index=True, nullable=False)
    customer_name = Column(String(200), nullable=False)
    customer_email = Column(String(200), nullable=False)
    shipping_address = Column(Text, nullable=False)
    items = Column(JSON, nullable=False)
    total_amount = Column(Float, nullable=False)
    status = Column(String(50), default="pending", nullable=False)  # paid, failed, pending
    payment_status = Column(String(50), nullable=False)             # approved, declined
    payment_error_reason = Column(String(100), nullable=True)
    transaction_id = Column(String(100), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())