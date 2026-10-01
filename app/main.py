import asyncio
import random
import uuid
from fastapi import FastAPI, Depends, HTTPException, status, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import text
from contextlib import asynccontextmanager
from typing import List, Optional
from datetime import datetime, timezone

from app.database import engine, Base, get_db, SessionLocal
from app.models import Product, Order
from app.schemas import (
    ProductCreate,
    ProductResponse,
    HealthResponse,
    OrderCreate,
    OrderResponse,
    SlowResponse,
)
from app.seed import seed_products
from app.payment import simulate_payment
from prometheus_fastapi_instrumentator import Instrumentator

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
    description="API de catálogo, pedidos y pagos para Manifest Supply Co.",
    version="2.0.0",
    lifespan=lifespan
)

# Instrumentar métricas Prometheus y exponer /metrics
Instrumentator().instrument(app).expose(app, endpoint="/metrics", tags=["Metrics"])

# Permitir CORS para que el frontend pueda comunicarse con esta API
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
        "metrics": "/metrics",
        "products": "/products",
        "orders": "/orders",
        "slow": "/slow"
    }

# --- 1. Endpoint /health ---
@app.get("/health", response_model=HealthResponse, tags=["Health"])
def health_check(db: Session = Depends(get_db)):
    db_status = "connected"
    try:
        db.execute(text("SELECT 1"))
    except Exception as e:
        db_status = f"disconnected: {str(e)}"

    return {
        "status": "healthy" if db_status == "connected" else "degraded",
        "database": db_status,
        "timestamp": datetime.now(timezone.utc)
    }

# --- 2. Endpoints de Productos ---
@app.get("/products", response_model=List[ProductResponse], tags=["Products"])
def get_products(category: Optional[str] = None, db: Session = Depends(get_db)):
    query = db.query(Product)
    if category and category.lower() != "all":
        query = query.filter(Product.category == category.lower())
    return query.all()

@app.get("/products/{product_id}", response_model=ProductResponse, tags=["Products"])
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Producto con id {product_id} no encontrado"
        )
    return product

@app.post("/products", response_model=ProductResponse, status_code=status.HTTP_201_CREATED, tags=["Products"])
def create_product(product_data: ProductCreate, db: Session = Depends(get_db)):
    new_product = Product(**product_data.model_dump())
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product

# --- 3. Endpoints de Órdenes y Pagos Simulados ---
@app.post("/orders", response_model=OrderResponse, status_code=status.HTTP_201_CREATED, tags=["Orders"])
def create_order(order_in: OrderCreate, db: Session = Depends(get_db)):
    # 1. Validar productos y calcular total real desde la base de datos
    order_items_detail = []
    total_amount = 0.0

    for item in order_in.items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Producto con ID {item.product_id} no existe en catálogo"
            )
        
        subtotal = round(product.price * item.quantity, 2)
        total_amount += subtotal
        order_items_detail.append({
            "product_id": product.id,
            "name": product.name,
            "price": product.price,
            "quantity": item.quantity,
            "subtotal": subtotal
        })

    total_amount = round(total_amount, 2)

    # 2. Simular pago (10% de probabilidad de fallo para pruebas de caos/incidentes)
    payment_result = simulate_payment(amount=total_amount, failure_rate=0.10)

    # 3. Generar número de orden con formato MSC de dropshipping
    order_num = f"MSC-{random.randint(1000, 9999)}-{random.randint(1000, 9999)}-{uuid.uuid4().hex[:2].upper()}"

    # 4. Crear la orden y persistirla en PostgreSQL (incluso si falló el pago para auditoría)
    order = Order(
        order_number=order_num,
        customer_name=order_in.customer_name,
        customer_email=order_in.customer_email,
        shipping_address=order_in.shipping_address,
        items=order_items_detail,
        total_amount=total_amount,
        status="paid" if payment_result.success else "failed",
        payment_status="approved" if payment_result.success else "declined",
        payment_error_reason=payment_result.reason,
        transaction_id=payment_result.transaction_id
    )

    db.add(order)
    db.commit()
    db.refresh(order)

    # 5. Si el pago fue rechazado, emitir HTTP 402 Payment Required para provocar incidente
    if not payment_result.success:
        raise HTTPException(
            status_code=status.HTTP_402_PAYMENT_REQUIRED,
            detail={
                "message": "Pago rechazado por la pasarela simulada",
                "order_number": order.order_number,
                "reason": payment_result.reason,
                "total_amount": order.total_amount,
                "order_id": order.id
            }
        )

    return order

@app.get("/orders", response_model=List[OrderResponse], tags=["Orders"])
def list_orders(order_status: Optional[str] = Query(None, alias="status"), db: Session = Depends(get_db)):
    query = db.query(Order)
    if order_status:
        query = query.filter(Order.status == order_status.lower())
    return query.order_by(Order.id.desc()).all()

@app.get("/orders/{order_id}", response_model=OrderResponse, tags=["Orders"])
def get_order(order_id: int, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Orden con id {order_id} no encontrada"
        )
    return order

@app.get("/orders/track/{order_number}", response_model=OrderResponse, tags=["Orders"])
def track_order(order_number: str, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.order_number == order_number.strip().upper()).first()
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se encontró ninguna orden con el número de rastreo {order_number}"
        )
    return order

# --- 4. Endpoint de Latencia Artificial /slow ---
@app.get("/slow", response_model=SlowResponse, tags=["Chaos & Performance"])
async def slow_endpoint(delay: float = Query(2.0, ge=0.1, le=30.0, description="Segundos de retraso artificial")):
    """
    Endpoint para probar latencia artificial, métricas p95/p99, y timeouts en Kubernetes / clientes.
    """
    await asyncio.sleep(delay)
    return {
        "status": "ok",
        "delay_seconds": delay,
        "message": f"Respuesta demorada artificialmente por {delay} segundos",
        "timestamp": datetime.now(timezone.utc)
    }