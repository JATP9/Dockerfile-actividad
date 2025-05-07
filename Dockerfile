# 1. Imagen base con Python
FROM python:3.12-slim

# 2. Establecer directorio de trabajo
WORKDIR /app

# 3. Copiar archivos de requerimientos
COPY requirements.txt .

# 4. Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copiar el resto del código fuente
COPY . .


# 7. Comando para ejecutar la aplicación
CMD ["python", "apidatos.py"]

