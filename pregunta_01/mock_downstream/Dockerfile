FROM python:3.11-slim

WORKDIR /app

RUN pip install --no-cache-dir fastapi uvicorn

COPY server.py .

EXPOSE 8080

ENV PYTHONUNBUFFERED=1
ENV DELAY_SECONDS=8.0

CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8080"]
