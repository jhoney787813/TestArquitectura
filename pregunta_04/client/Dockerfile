FROM python:3.11-slim

WORKDIR /app

COPY websocket_client.html /app/index.html

EXPOSE 8084

CMD ["python", "-m", "http.server", "8084"]
