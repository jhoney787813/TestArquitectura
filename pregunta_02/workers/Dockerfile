FROM python:3.11-slim

WORKDIR /app

RUN pip install --no-cache-dir fastapi uvicorn httpx

COPY notification_worker.py .

EXPOSE 8090

ENV PYTHONUNBUFFERED=1
ENV GATEWAY_URL="http://mock-gateways:8091"

CMD ["uvicorn", "notification_worker:app", "--host", "0.0.0.0", "--port", "8090"]
