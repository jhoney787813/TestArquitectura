import os
import asyncio
import time
from fastapi import FastAPI, Response
from datetime import datetime

app = FastAPI(title="Mock External Gateways (Email, SMS, Audit Service)")

# Colores ANSI
COLOR_CYAN = "\033[96m"
COLOR_YELLOW = "\033[93m"
COLOR_GREEN = "\033[92m"
COLOR_RED = "\033[91m"
COLOR_RESET = "\033[0m"

# Estado de Circuit Breaker para SMS
circuit_breaker_sms = {
    "failures": 0,
    "state": "CLOSED", # CLOSED, OPEN, HALF_OPEN
    "last_failure_time": 0
}

@app.get("/health")
async def health():
    return {"status": "UP", "sms_circuit_breaker": circuit_breaker_sms}

# ✉️ GATEWAY DE EMAIL (Pregunta C)
@app.post("/api/v1/send-email")
async def send_email(payload: dict):
    policy_id = payload.get("policy_id", "UNKNOWN")
    simulate = payload.get("simulate_fail", "none")
    now_str = datetime.now().strftime("%H:%M:%S.%f")[:-3]

    if simulate == "email":
        print(f"{COLOR_RED}[{now_str}] ❌ [EMAIL GATEWAY FALLIDO] Error enviando correo para Póliza {policy_id} (Servidor SMTP Down / Timeout){COLOR_RESET}", flush=True)
        return Response(status_code=503, content='{"status": "ERROR", "error": "SMTP Gateway Unavailable"}', media_type="application/json")

    print(f"{COLOR_GREEN}[{now_str}] 📧 [EMAIL ENVIADO ✅] Correo de Póliza {policy_id} entregado al cliente.{COLOR_RESET}", flush=True)
    return {"status": "DELIVERED", "channel": "EMAIL", "policy_id": policy_id}


# 📱 GATEWAY DE SMS CON CIRCUIT BREAKER (Pregunta D)
@app.post("/api/v1/send-sms")
async def send_sms(payload: dict):
    policy_id = payload.get("policy_id", "UNKNOWN")
    simulate = payload.get("simulate_fail", "none")
    now_str = datetime.now().strftime("%H:%M:%S.%f")[:-3]

    # Verificar si el Circuit Breaker está ABIERTO
    if circuit_breaker_sms["state"] == "OPEN":
        if time.time() - circuit_breaker_sms["last_failure_time"] > 10:
            circuit_breaker_sms["state"] = "HALF_OPEN"
            print(f"{COLOR_YELLOW}[{now_str}] 🟡 [CIRCUIT BREAKER SMS] Estado: HALF-OPEN. Probando salud del gateway...{COLOR_RESET}", flush=True)
        else:
            print(f"{COLOR_RED}[{now_str}] ⚡ [CIRCUIT BREAKER SMS - ABIERTO 🔴] Petición SMS cortada inmediatamente (Fallback a Push / Queue). Póliza {policy_id} no afectada.{COLOR_RESET}", flush=True)
            return Response(status_code=503, content='{"status": "CIRCUIT_OPEN", "fallback": "PUSH_NOTIFICATION_SENT"}', media_type="application/json")

    if simulate == "sms":
        circuit_breaker_sms["failures"] += 1
        circuit_breaker_sms["last_failure_time"] = time.time()
        
        if circuit_breaker_sms["failures"] >= 2:
            circuit_breaker_sms["state"] = "OPEN"
            print(f"{COLOR_RED}[{now_str}] ⚡ [CIRCUIT BREAKER SMS TRIPPED! 🔴] 2 fallas consecutivas detectadas. CIRCUITO ABIERTO para proteger el sistema.{COLOR_RESET}", flush=True)
        else:
            print(f"{COLOR_RED}[{now_str}] ❌ [SMS FALLIDO] Falla de proveedor SMS para Póliza {policy_id} (Falla {circuit_breaker_sms['failures']}/2){COLOR_RESET}", flush=True)

        return Response(status_code=500, content='{"status": "ERROR", "error": "SMS Telephony Gateway Down"}', media_type="application/json")

    # Si fue exitoso y estaba en HALF_OPEN -> CERRAR CIRCUITO
    circuit_breaker_sms["state"] = "CLOSED"
    circuit_breaker_sms["failures"] = 0
    print(f"{COLOR_GREEN}[{now_str}] 📱 [SMS ENVIADO ✅] Mensaje SMS entregado para Póliza {policy_id}.{COLOR_RESET}", flush=True)
    return {"status": "DELIVERED", "channel": "SMS", "policy_id": policy_id}


# 🔍 SERVICIO DE AUDITORÍA CENTRALIZADA - ELASTICSEARCH/OPENSEARCH (Pregunta E)
@app.post("/api/v1/audit-ingest")
async def audit_ingest(payload: dict):
    policy_id = payload.get("policy_id", "UNKNOWN")
    simulate = payload.get("simulate_fail", "none")
    now_str = datetime.now().strftime("%H:%M:%S.%f")[:-3]

    if simulate == "audit":
        print(f"{COLOR_RED}[{now_str}] ❌ [AUDIT SERVICE FALLIDO] ElasticSearch/OpenSearch no responde para Póliza {policy_id}{COLOR_RESET}", flush=True)
        print(f"{COLOR_YELLOW}[{now_str}] 🔒 [AUDITORÍA PRESERVADA] La auditoría local en la BD de la Póliza se mantiene intacta. El evento reintentará ingresar al cluster central.{COLOR_RESET}", flush=True)
        return Response(status_code=503, content='{"status": "ERROR", "error": "Centralized Audit Indexing Timeout"}', media_type="application/json")

    print(f"{COLOR_CYAN}[{now_str}] 🔍 [AUDITORÍA CENTRALIZADA ✅] Evento de Póliza {policy_id} indexado en OpenSearch / ElasticSearch Log Index.{COLOR_RESET}", flush=True)
    return {"status": "INDEXED", "store": "OpenSearch_Cluster_v2.1", "policy_id": policy_id}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8091)
