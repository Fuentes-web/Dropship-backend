# 1. Imagen base oficial de Python ligera basada en Debian
FROM python:3.11-slim

# 2. Buenas prácticas para entornos de producción y contenedores
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 3. Carpeta de trabajo dentro del contenedor
WORKDIR /app

# 4. Instalamos curl para healthchecks del contenedor y herramientas de red
RUN apt-get update && apt-get install -y --no-install-recommends curl && rm -rf /var/lib/apt/lists/*

# 5. Copiamos requirements.txt e instalamos dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 6. Copiamos el código fuente de la aplicación
COPY app/ ./app/

# 7. Exponemos el puerto estándar de FastAPI
EXPOSE 8000

# 8. Arrancamos el servidor Uvicorn con recarga en caliente para desarrollo
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
