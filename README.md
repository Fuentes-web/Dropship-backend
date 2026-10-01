# Dropshipping Store — Backend API

Backend profesional para la plataforma de dropshipping, desarrollado con **FastAPI**, persistencia en **PostgreSQL**, contenedorizado con **Docker & Docker Compose**, y preparado para orquestación en **Kubernetes (`k8s/`)**.

---

## 📁 Estructura del Proyecto

```text
dropship-backend/
├── app/                      # Código fuente de la API
│   ├── __init__.py
│   ├── database.py           # Conexión SQLAlchemy y get_db
│   ├── models.py             # Modelo ORM de Producto
│   ├── schemas.py            # Esquemas Pydantic v2
│   ├── seed.py               # Productos de prueba del catálogo
│   └── main.py               # Aplicación FastAPI, CORS y endpoints
├── docker/                   # Contenedores e infraestructura local
│   ├── Dockerfile            # Imagen ligera con Python 3.11-slim
│   ├── docker-compose.yml    # Orquestación de API + PostgreSQL 16
│   └── .env.example          # Plantilla de variables de entorno
├── k8s/                      # Manifiestos de Kubernetes para producción
│   ├── configmap.yaml        # Configuración no confidencial
│   ├── secret.yaml           # Credenciales seguras
│   ├── postgres-pvc.yaml     # Volumen persistente de almacenamiento
│   ├── postgres-deployment.yaml # Despliegue y servicio de PostgreSQL
│   └── api-deployment.yaml   # Despliegue y servicio NodePort de la API
├── .gitignore                # Reglas de exclusión para Git
├── requirements.txt          # Dependencias de Python
└── README.md                 # Documentación del proyecto
```

---

## 🚀 Inicio Rápido con Docker Compose (Recomendado)

La forma más rápida de levantar tanto la base de datos PostgreSQL como la API de FastAPI es usando Docker Compose.

### 1. Requisitos
- **Docker Desktop** instalado y en ejecución en tu equipo.

### 2. Levantar los servicios
Desde la carpeta raíz del backend, ejecuta:

```bash
cd docker
docker compose up -d
```

*(El parámetro `-d` levanta los contenedores en segundo plano y deja tu terminal libre).*

### 3. Verificar el estado
```bash
docker compose ps
```

### 4. Ver los logs en tiempo real
```bash
docker compose logs -f
```
*(Presiona `Ctrl + C` para salir de los logs sin apagar los contenedores).*

### 5. Apagar los servicios
```bash
docker compose down
```

---

## 🌐 Endpoints de la API

Con los contenedores arriba, abre en tu navegador:

| Método | Endpoint | Descripción |
|---|---|---|
| `GET` | [`/`](http://localhost:8000/) | Mensaje de bienvenida y enlaces principales |
| `GET` | [`/health`](http://localhost:8000/health) | Estado del servicio y conectividad con PostgreSQL |
| `GET` | [`/products`](http://localhost:8000/products) | Lista de productos (con filtro opcional `?category=audio`) |
| `GET` | [`/products/{id}`](http://localhost:8000/products/1) | Detalle de un producto individual |
| `POST` | [`/products`](http://localhost:8000/products) | Crear un nuevo producto en catálogo |
| `GET` | [`/docs`](http://localhost:8000/docs) | **Swagger UI:** Documentación interactiva para probar peticiones |
| `GET` | [`/redoc`](http://localhost:8000/redoc) | Documentación técnica alternativa ReDoc |

---

## 💻 Ejecución Local con Python (Sin Docker)

Si prefieres correr la API directamente en tu máquina:

### 1. Crear y activar entorno virtual
```bash
# Crear entorno virtual
python -m venv .venv

# Activar en Git Bash:
source .venv/Scripts/activate

# O activar en PowerShell:
# .\.venv\Scripts\Activate.ps1
```

### 2. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 3. Iniciar el servidor
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

---

## ☸️ Despliegue en Kubernetes (`k8s/`)

Para desplegar en Minikube, Kind o cualquier clúster de Kubernetes:

```bash
# 1. Aplicar secretos y configuraciones
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/secret.yaml

# 2. Desplegar almacenamiento y PostgreSQL
kubectl apply -f k8s/postgres-pvc.yaml
kubectl apply -f k8s/postgres-deployment.yaml

# 3. Desplegar la API FastAPI
kubectl apply -f k8s/api-deployment.yaml

# 4. Verificar pods y servicios
kubectl get pods
kubectl get svc
```

La API quedará expuesta en el puerto **30080** del clúster.

---

## 📤 Conectar y Subir a GitHub

Si ya creaste el repositorio en GitHub, sigue estos pasos para subir todo tu código:

```bash
# 1. Asegúrate de estar en la carpeta dropship-backend
cd /c/Users/luisa/Downloads/Dropshipping/dropship-backend

# 2. Agregar todos los archivos
git add .

# 3. Crear el commit
git commit -m "feat: complete dropshipping backend with FastAPI, Docker and K8s"

# 4. Enlazar con tu repositorio remoto de GitHub (reemplaza con tu URL real)
git remote add origin https://github.com/Fuentes-web/<TU-REPOSITORIO>.git

# 5. Asegurar rama main y subir cambios
git branch -M main
git push -u origin main
```
