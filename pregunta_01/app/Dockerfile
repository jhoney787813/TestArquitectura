FROM python:3.11-slim

WORKDIR /app

# Instalar dependencias necesarias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código de la aplicación
COPY main.py .

EXPOSE 8000

ENV PYTHONUNBUFFERED=1
ENV DOWNSTREAM_URL="http://mock-downstream:8080/api/v1/external-data"
ENV MAX_CONCURRENT_CONNECTIONS=5

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "2"]
