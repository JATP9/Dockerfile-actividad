# 1. Imagen base con Python
FROM python:3.11-slim

# 2. Establecer directorio de trabajo
WORKDIR /app

# 3. Copiar archivos de requerimientos
COPY requirements.txt .

# 4. Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copiar el resto del código fuente
COPY . .

# 6. Exponer el puerto de la app
EXPOSE 5000

# 7. Comando para ejecutar la aplicación
CMD ["python", "app.py"]

