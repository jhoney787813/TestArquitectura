FROM python:3.11-slim

WORKDIR /app

RUN pip install --no-cache-dir httpx

COPY event_generator.py .

ENV PYTHONUNBUFFERED=1
ENV GATEWAY_URL="http://realtime-api:8000/api/v1/realtime/publish-event"

CMD ["python", "event_generator.py"]
