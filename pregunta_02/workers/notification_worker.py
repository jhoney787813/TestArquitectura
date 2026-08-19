import os
import asyncio
import time
import httpx
from fastapi import FastAPI, Response
from datetime import datetime

app = FastAPI(title="Worker de Procesamiento de Eventos Outbox (Notificaciones & Auditoría)")

GATEWAY_URL = os.getenv("GATEWAY_URL", "http://mock-gateways:8091")

# Cola de eventos caídos (Dead Letter Queue - DLQ)
dead_letter_queue = []

COLOR_CYAN = "\033[96m"
COLOR_YELLOW = "\033[93m"
COLOR_GREEN = "\033[92m"
COLOR_RED = "\033[91m"
COLOR_RESET = "\033[0m"

@app.get("/health")
async def health():
    return {"status": "UP", "dlq_count": len(dead_letter_queue)}

@app.get("/api/v1/dlq")
async def get_dlq():
    return {"dlq_total": len(dead_letter_queue), "messages": dead_letter_queue}

# 🟢 RECEPTOR DE EVENTOS DE OUTBOX
@app.post("/process-event")
async def process_event(event: dict):
    policy_id = event.get("policy_id", "UNKNOWN")
    simulate = event.get("simulate_fail", "none")
    now_str = datetime.now().strftime("%H:%M:%S.%f")[:-3]

    print(f"\n{COLOR_CYAN}[{now_str}] ⚙️ [WORKER ASÍNCRONO] Procesando Evento Outbox '{event.get('event_type')}' para Póliza {policy_id}...{COLOR_RESET}", flush=True)

    async with httpx.AsyncClient(timeout=5.0) as client:
        # 1. PROCESAR EMAIL (Pregunta C)
        email_success = await process_channel(client, f"{GATEWAY_URL}/api/v1/send-email", event, "EMAIL")
        
        # 2. PROCESAR SMS (Pregunta D)
        sms_success = await process_channel(client, f"{GATEWAY_URL}/api/v1/send-sms", event, "SMS")
        
        # 3. PROCESAR AUDITORÍA CENTRALIZADA (Pregunta E)
        audit_success = await process_channel(client, f"{GATEWAY_URL}/api/v1/audit-ingest", event, "AUDIT")

    now_end = datetime.now().strftime("%H:%M:%S.%f")[:-3]
    print(f"{COLOR_GREEN}[{now_end}] ✅ [WORKER COMPLETADO] Evento Outbox para Póliza {policy_id} procesado.{COLOR_RESET}\n", flush=True)
    return {"status": "PROCESSED", "policy_id": policy_id}

async def process_channel(client: httpx.AsyncClient, url: str, event: dict, channel_name: str) -> bool:
    policy_id = event.get("policy_id")
    max_retries = 2
    
    for attempt in range(1, max_retries + 1):
        try:
            res = await client.post(url, json=event)
            if res.status_code == 200:
                return True
            
            now_str = datetime.now().strftime("%H:%M:%S.%f")[:-3]
            print(f"{COLOR_YELLOW}[{now_str}] ⚠️ [{channel_name} RETRY {attempt}/{max_retries}] Falla temporal en canal {channel_name} (HTTP {res.status_code}){COLOR_RESET}", flush=True)
            await asyncio.sleep(0.5 * attempt) # Exponential backoff
        except Exception as e:
            now_str = datetime.now().strftime("%H:%M:%S.%f")[:-3]
            print(f"{COLOR_RED}[{now_str}] ❌ [{channel_name} EXCEPCIÓN] Error de conexión: {e}{COLOR_RESET}", flush=True)

    # Si fallan todos los reintentos -> Encolar en DLQ (Dead Letter Queue)
    now_dlq = datetime.now().strftime("%H:%M:%S.%f")[:-3]
    print(f"{COLOR_RED}[{now_dlq}] 📥 [ENCOLADO EN DLQ] Canal {channel_name} falló permanentemente. Evento enviado a Dead Letter Queue para Póliza {policy_id}{COLOR_RESET}", flush=True)
    dead_letter_queue.append({
        "timestamp": now_dlq,
        "channel": channel_name,
        "policy_id": policy_id,
        "event": event,
        "reason": f"Max retries ({max_retries}) exceeded or Circuit Breaker Open"
    })
    return False

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8090)
