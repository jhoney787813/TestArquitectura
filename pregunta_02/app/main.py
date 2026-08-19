import os
import asyncio
import time
import uuid
import httpx
from fastapi import FastAPI, Response, status, Query
from pydantic import BaseModel
from datetime import datetime

app = FastAPI(
    title="API de Emisión de Pólizas - Ejercicio 2 (Transactional Outbox Pattern)",
    description="Simulación de arquitectura resiliente con Transactional Outbox, Circuit Breakers, Retries y DLQ.",
    version="2.0.0"
)

# Base de datos simulada en memoria con soporte ACID local
db_policies = {}
db_local_audit = {}
db_outbox_events = []

WORKER_URL = os.getenv("WORKER_URL", "http://notification-worker:8090/process-event")

# Colores ANSI para logs visuales en consola
COLOR_CYAN = "\033[96m"
COLOR_YELLOW = "\033[93m"
COLOR_GREEN = "\033[92m"
COLOR_RED = "\033[91m"
COLOR_BOLD = "\033[1m"
COLOR_RESET = "\033[0m"

class EmitPolicyRequest(BaseModel):
    customer_name: str
    insured_amount: float
    policy_type: str = "AUTO_GLOBAL"

@app.get("/health")
async def health():
    return {"status": "UP", "policies_emitted": len(db_policies)}

@app.get("/api/v1/outbox")
async def get_outbox():
    return {
        "total_outbox_events": len(db_outbox_events),
        "events": db_outbox_events
    }

@app.get("/api/v1/policies/{policy_id}")
async def get_policy(policy_id: str):
    if policy_id not in db_policies:
        return Response(status_code=404, content='{"error": "Policy not found"}', media_type="application/json")
    return {
        "policy": db_policies[policy_id],
        "local_audit": db_local_audit.get(policy_id, [])
    }

# 🚀 ENDPOINT PRINCIPAL: EMISIÓN DE PÓLIZA CON TRANSACTIONAL OUTBOX
@app.post("/api/v1/policies/emit")
async def emit_policy(
    request: EmitPolicyRequest,
    simulate_fail: str = Query("none", description="Simular fallas: 'save_policy', 'email', 'sms', 'audit'")
):
    start_time = time.time()
    now_str = datetime.now().strftime("%H:%M:%S.%f")[:-3]
    policy_id = f"POL-{str(uuid.uuid4())[:8].upper()}"

    print(f"\n{COLOR_CYAN}[{now_str}] 📩 [PETICIÓN RECIBIDA] Emisión de Póliza para: {request.customer_name} | Simulación: '{simulate_fail}'{COLOR_RESET}", flush=True)

    # 🔴 ESCENARIO B: ¿Qué pasa si SavePolicy falla?
    if simulate_fail == "save_policy":
        now_err = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        print(f"{COLOR_RED}[{now_err}] ❌ [ERROR B] SavePolicy falló (Error de BD / Restricción de Integridad). Ejecutando ROLLBACK ACID...{COLOR_RESET}", flush=True)
        print(f"{COLOR_RED}[{now_err}] 🛑 [ROLLBACK] Ningún registro guardado, NINGÚN evento Outbox creado, NINGÚN email/SMS enviado.{COLOR_RESET}\n", flush=True)
        return Response(
            status_code=500,
            content=f'{{"status": "ERROR", "message": "SavePolicy failed. Transaction rolled back completely.", "policy_created": false}}',
            media_type="application/json"
        )

    # 🟢 1. INICIO DE TRANSACCIÓN ACID LOCAL (`BEGIN TRANSACTION`)
    # Pasos A y E: Actualizar DB + Auditoría Local en la MISMA transacción
    now_tx = datetime.now().strftime("%H:%M:%S.%f")[:-3]
    print(f"{COLOR_YELLOW}[{now_tx}] ⚙️ [TRANSACCIÓN LOCAL ACID] Guardando Póliza {policy_id} + Registrando Auditoría Local...{COLOR_RESET}", flush=True)

    db_policies[policy_id] = {
        "policy_id": policy_id,
        "customer_name": request.customer_name,
        "insured_amount": request.insured_amount,
        "policy_type": request.policy_type,
        "status": "EMITTED",
        "created_at": now_tx,
        "email_status": "PENDING",
        "sms_status": "PENDING",
        "audit_external_status": "PENDING"
    }

    # Auditoría Local (Persistida en la misma DB de la póliza)
    db_local_audit[policy_id] = [{
        "timestamp": now_tx,
        "action": "POLICY_EMITTED_LOCAL",
        "detail": f"Póliza {policy_id} emitida y persistida en BD local."
    }]

    # Transactional Outbox Event
    outbox_event = {
        "event_id": f"EVT-{str(uuid.uuid4())[:8].upper()}",
        "policy_id": policy_id,
        "event_type": "POLICY_EMITTED",
        "customer_name": request.customer_name,
        "simulate_fail": simulate_fail,
        "status": "PENDING",
        "created_at": now_tx
    }
    db_outbox_events.append(outbox_event)

    now_commit = datetime.now().strftime("%H:%M:%S.%f")[:-3]
    print(f"{COLOR_GREEN}[{now_commit}] ✅ [COMMIT LOCAL] Póliza {policy_id} y Evento Outbox guardados en BD local (Latencia DB: {(time.time()-start_time)*1000:.2f}ms){COLOR_RESET}", flush=True)

    # 🟢 2. DESPACHO ASÍNCRONO DEL EVENTO (Worker en segundo plano sin bloquear HTTP)
    asyncio.create_task(dispatch_event_to_worker(outbox_event))

    elapsed = time.time() - start_time
    print(f"{COLOR_BOLD}{COLOR_GREEN}[{now_commit}] 🚀 [RESPUESTA HTTP 201] Póliza emitida exitosamente en {elapsed*1000:.2f}ms al cliente.{COLOR_RESET}\n", flush=True)

    return {
        "status": "SUCCESS",
        "message": "Policy emitted successfully",
        "policy_id": policy_id,
        "response_time_ms": round(elapsed * 1000, 2),
        "note": "Notificaciones (Email/SMS) y Auditoría Centralizada se procesan asíncronamente vía Outbox."
    }

async def dispatch_event_to_worker(event: dict):
    """Envía el evento Outbox al Worker en segundo plano de manera no bloqueante"""
    await asyncio.sleep(0.1)
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            await client.post(WORKER_URL, json=event)
    except Exception as e:
        print(f"{COLOR_RED}⚠️ Error conectando al worker de eventos: {e}{COLOR_RESET}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
