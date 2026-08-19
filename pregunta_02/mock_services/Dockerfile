FROM python:3.11-slim

WORKDIR /app

RUN pip install --no-cache-dir fastapi uvicorn httpx

COPY external_gateways.py .

EXPOSE 8091

ENV PYTHONUNBUFFERED=1

CMD ["uvicorn", "external_gateways:app", "--host", "0.0.0.0", "--port", "8091"]
