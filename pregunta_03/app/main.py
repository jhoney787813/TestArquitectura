import os
import asyncio
import time
import json
import uuid
from typing import List
from datetime import datetime
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Response, Query
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

app = FastAPI(
    title="Real-Time Gateway API - Ejercicio 3 (SignalR / WebSockets / SSE / Kafka Backbone)",
    description="Gateway en tiempo real para rastreo de Emisión, Inspección y Siniestros mediante SSE, WebSockets, SignalR y Polling.",
    version="3.0.0"
)

# Bus de eventos en memoria simulando Kafka Event Consumer & Redis Pub/Sub Backplane
event_subscribers: List[asyncio.Queue] = []
active_websockets: List[WebSocket] = []

# Historial de estados en tiempo real
realtime_store = {
    "emision": {"policy_id": "POL-1001", "status": "EMITTED", "updated_at": "Init"},
    "inspeccion": {"inspection_id": "INS-5002", "status": "INSPECTOR_ASSIGNED", "updated_at": "Init"},
    "siniestros": {"claim_id": "CLM-9003", "status": "CLAIM_FILED", "updated_at": "Init"}
}

# Colores ANSI para terminal
COLOR_CYAN = "\033[96m"
COLOR_YELLOW = "\033[93m"
COLOR_GREEN = "\033[92m"
COLOR_MAGENTA = "\033[95m"
COLOR_BOLD = "\033[1m"
COLOR_RESET = "\033[0m"

class RealtimeEventPayload(BaseModel):
    event_type: str # "emision", "inspeccion", "siniestros"
    entity_id: str
    status: str
    detail: str = ""

@app.get("/health")
async def health():
    return {
        "status": "UP",
        "active_sse_subscribers": len(event_subscribers),
        "active_websockets": len(active_websockets),
        "store": realtime_store
    }

# 🚀 ENDPOINT INTERNO: INGESTA DE EVENTOS (Simulando Kafka Event Consumer)
@app.post("/api/v1/realtime/publish-event")
async def publish_event(payload: RealtimeEventPayload):
    now_str = datetime.now().strftime("%H:%M:%S.%f")[:-3]
    event_data = {
        "event_id": f"EVT-{str(uuid.uuid4())[:8].upper()}",
        "category": payload.event_type,
        "entity_id": payload.entity_id,
        "status": payload.status,
        "detail": payload.detail,
        "timestamp": now_str
    }

    # Actualizar estado global
    realtime_store[payload.event_type] = event_data

    print(f"\n{COLOR_CYAN}[{now_str}] 📢 [KAFKA EVENT CONSUMED] Categoría: {payload.event_type.upper()} | ID: {payload.entity_id} | Estado: {payload.status}{COLOR_RESET}", flush=True)

    # Broadcast a suscriptores SSE
    for queue in event_subscribers:
        await queue.put(event_data)

    # Broadcast a suscriptores WebSockets / SignalR
    disconnected_ws = []
    for ws in active_websockets:
        try:
            await ws.send_text(json.dumps(event_data))
        except Exception:
            disconnected_ws.append(ws)

    for ws in disconnected_ws:
        if ws in active_websockets:
            active_websockets.remove(ws)

    return {"status": "BROADCAST_SUCCESS", "subscribers_notified": len(event_subscribers) + len(active_websockets)}


# 🟢 TECNOLOGÍA 1: SERVER-SENT EVENTS (SSE) (Server-to-Client Stream HTTP/2)
@app.get("/api/v1/realtime/stream")
async def sse_stream():
    """
    Server-Sent Events (SSE): Flujo unidireccional continuo sobre HTTP.
    Ideal para dashboards de lectura en tiempo real (Emisión, Inspección, Siniestros).
    """
    queue = asyncio.Queue()
    event_subscribers.append(queue)
    now_str = datetime.now().strftime("%H:%M:%S.%f")[:-3]
    print(f"{COLOR_GREEN}[{now_str}] 🔌 [NUEVA CONEXIÓN SSE] Cliente suscrito al stream HTTP de eventos.{COLOR_RESET}", flush=True)

    async def event_generator():
        try:
            # Enviar evento de bienvenida inmediato
            welcome = {"type": "CONNECTED", "message": "Suscripción SSE activa en tiempo real."}
            yield f"data: {json.dumps(welcome)}\n\n"

            while True:
                data = await queue.get()
                yield f"data: {json.dumps(data)}\n\n"
        except asyncio.CancelledError:
            print(f"{COLOR_YELLOW}⚠️ Cliente SSE desconectado.{COLOR_RESET}")
        finally:
            if queue in event_subscribers:
                event_subscribers.remove(queue)

    return StreamingResponse(event_generator(), media_type="text/event-stream")


# 🟢 TECNOLOGÍA 2: WEBSOCKETS (Full-Duplex Bidireccional TCP)
@app.websocket("/api/v1/realtime/ws")
async def websocket_endpoint(websocket: WebSocket):
    """
    WebSockets: Conexión persistente bi-direccional Full-Duplex TCP.
    Permite enviar y recibir mensajes síncronos y asíncronos en tiempo real.
    """
    await websocket.accept()
    active_websockets.append(websocket)
    now_str = datetime.now().strftime("%H:%M:%S.%f")[:-3]
    print(f"{COLOR_MAGENTA}[{now_str}] ⚡ [NUEVA CONEXIÓN WEBSOCKET] Cliente bi-direccional conectado.{COLOR_RESET}", flush=True)

    try:
        await websocket.send_text(json.dumps({"type": "WS_CONNECTED", "store": realtime_store}))
        while True:
            # Escuchar mensajes entrantes del cliente
            msg = await websocket.receive_text()
            print(f"{COLOR_YELLOW}[WS INCOMING] Mensaje recibido del cliente: {msg}{COLOR_RESET}")
            # Echo de confirmación
            await websocket.send_text(json.dumps({"type": "ACK", "echo": msg, "timestamp": datetime.now().isoformat()}))
    except WebSocketDisconnect:
        print(f"{COLOR_YELLOW}⚠️ Cliente WebSocket desconectado.{COLOR_RESET}")
    finally:
        if websocket in active_websockets:
            active_websockets.remove(websocket)


# 🟢 TECNOLOGÍA 3: SIMULACIÓN DE SIGNALR HUB (.NET SignalR Protocol Abstraction)
@app.get("/api/v1/realtime/signalr-hub")
async def signalr_hub_info():
    """
    SignalR Abstraction Hub:
    Simula la negociación automática de SignalR:
    1. Trata de conectar WebSockets.
    2. Si falla o hay proxy estricto, conmuta a Server-Sent Events (SSE).
    3. Si es browser legacy, cae a Long Polling.
    """
    return {
        "framework": "SignalR Hub Core v8.0",
        "transport_negotiation": [
            {"transport": "WebSockets", "status": "AVAILABLE", "recommended": True},
            {"transport": "ServerSentEvents", "status": "AVAILABLE", "recommended": False},
            {"transport": "LongPolling", "status": "FALLBACK_AVAILABLE", "recommended": False}
        ],
        "redis_backplane": "ENABLED (Cluster Scale-out Across Nodes)",
        "current_status": realtime_store
    }


# 🔴 TECNOLOGÍA 4: POLLING (Short Polling vs Long Polling Comparison)
@app.get("/api/v1/realtime/polling")
async def polling_endpoint(
    mode: str = Query("short", description="Modo: 'short' (Instantáneo) o 'long' (Hold HTTP request)")
):
    """
    Polling Endpoint para comparación de ineficiencia frente a WebSockets/SSE.
    - Short Polling: Responde de inmediato. 95% de llamadas traen datos sin cambios.
    - Long Polling: Retiene la petición HTTP hasta 5 segundos esperando cambios.
    """
    start_time = time.time()
    
    if mode == "long":
        # Retener la petición 3 segundos para simular Long Polling
        await asyncio.sleep(3.0)
        elapsed = time.time() - start_time
        return {
            "mode": "LONG_POLLING",
            "held_time_seconds": round(elapsed, 2),
            "data": realtime_store
        }

    # Short Polling instantáneo
    return {
        "mode": "SHORT_POLLING",
        "data": realtime_store,
        "inefficiency_note": "Short polling consume CPU y ancho de banda en peticiones repetitivas sin cambios."
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
