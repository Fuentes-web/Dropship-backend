# 1. Imagen base oficial de Python ligera basada en Debian
FROM python:3.11-slim

# 2. Buenas prácticas para entornos de producción y contenedores
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 3. Carpeta de trabajo dentro del contenedor
WORKDIR /app

# 4. Copiamos requirements.txt e instalamos dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copiamos el código fuente de la aplicación
COPY app/ ./app/

# 6. Exponemos el puerto estándar de FastAPI
EXPOSE 8000

# 7. Arrancamos el servidor Uvicorn con recarga en caliente para desarrollo
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
