import http from 'k6/http';
import { check, sleep } from 'k6';

// 1. Configuracion de la prueba de carga
export const options = {
  stages: [
    { duration: '10s', target: 10 }, // Ramp-up a 10 usuarios virtuales (VUs)
    { duration: '20s', target: 20 }, // Carga sostenida con hasta 20 VUs
    { duration: '10s', target: 0 },  // Ramp-down a 0 VUs
  ],
  thresholds: {
    // Al menos el 95% de las llamadas deben responder en menos de 1000ms
    http_req_duration: ['p(95)<1000'],
  },
};

const BASE_URL = __ENV.TARGET_URL || 'http://api:8000';

export default function () {
  const rand = Math.random();

  if (rand < 0.70) {
    // 70% del trafico: Exploracion de catalogo (GET /products)
    const res = http.get(`${BASE_URL}/products`);
    check(res, {
      'products status 200': (r) => r.status === 200,
    });
  } else if (rand < 0.85) {
    // 15% del trafico: Crear orden con simulacion de pago (POST /orders)
    // Nota: El simulador de pago genera ~10% de rechazos (HTTP 402) intencionales
    const payload = JSON.stringify({
      customer_name: `Customer VU-${__VU}`,
      customer_email: `user${__VU}_${__ITER}@example.com`,
      shipping_address: 'Av. Siempre Viva 742, Springfield',
      items: [
        {
          product_id: Math.floor(Math.random() * 5) + 1,
          quantity: Math.floor(Math.random() * 3) + 1,
        },
      ],
    });

    const headers = { 'Content-Type': 'application/json' };
    const res = http.post(`${BASE_URL}/orders`, payload, { headers });

    // Validamos que sea 201 (aprobado) o 402 (rechazado por el simulador de incidentes)
    check(res, {
      'order handled (201 or 402)': (r) => r.status === 201 || r.status === 402,
    });
  } else if (rand < 0.95) {
    // 10% del trafico: Inyeccion de latencia artificial (GET /slow)
    const res = http.get(`${BASE_URL}/slow?delay=0.3`);
    check(res, {
      'slow status 200': (r) => r.status === 200,
    });
  } else {
    // 5% del trafico: Health check (GET /health)
    const res = http.get(`${BASE_URL}/health`);
    check(res, {
      'health status 200': (r) => r.status === 200,
    });
  }

  // Pausa realista entre acciones de usuario
  sleep(0.3);
}
