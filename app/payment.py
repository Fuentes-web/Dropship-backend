import random
import uuid
from typing import Optional
from pydantic import BaseModel

class PaymentResult(BaseModel):
    success: bool
    transaction_id: Optional[str] = None
    reason: Optional[str] = None

# Razones de rechazo comunes en pasarelas reales (Stripe, PayPal)
FAILURE_REASONS = [
    "card_declined",
    "insufficient_funds",
    "gateway_timeout",
    "fraud_suspected"
]

def simulate_payment(amount: float, failure_rate: float = 0.10) -> PaymentResult:
    """
    Simula una pasarela de pago bancaria.
    Por defecto tiene una tasa de fallo del 10% (0.10) para pruebas de caos e incidentes.
    """
    # Genera un número aleatorio entre 0.0 y 1.0
    random_sample = random.random()

    if random_sample < failure_rate:
        # Fallo simulado (10% de las veces)
        reason = random.choice(FAILURE_REASONS)
        return PaymentResult(
            success=False,
            transaction_id=None,
            reason=reason
        )

    # Pago aprobado (90% de las veces)
    tx_id = f"txn_{uuid.uuid4().hex[:12]}"
    return PaymentResult(
        success=True,
        transaction_id=tx_id,
        reason=None
    )
