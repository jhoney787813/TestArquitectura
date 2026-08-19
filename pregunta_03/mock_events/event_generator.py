import os
import time
import random
import httpx
import asyncio

GATEWAY_URL = os.getenv("GATEWAY_URL", "http://realtime-api:8000/api/v1/realtime/publish-event")

STATUS_SEQUENCES = {
    "emision": [
        ("POL-1010", "POLICY_SUBMITTED", "Solicitud de póliza recibida en sistema core"),
        ("POL-1010", "RISK_EVALUATION", "Evaluando scoring de riesgo crediticio"),
        ("POL-1010", "POLICY_EMITTED", "Póliza emitida exitosamente"),
        ("POL-1010", "POLICY_ACTIVE", "Póliza activa y con cobertura vigente")
    ],
    "inspeccion": [
        ("INS-5050", "INSPECTION_REQUESTED", "Inspección de vehículo solicitada por el cliente"),
        ("INS-5050", "INSPECTOR_ASSIGNED", "Perito asignado: Ing. Roberto Gómez"),
        ("INS-5050", "INSPECTOR_ON_WAY", "Perito en camino a la ubicación del vehículo (GPS tracking)"),
        ("INS-5050", "INSPECTION_PASSED", "Inspección aprobada sin hallazgos de daños preexistentes")
    ],
    "siniestros": [
        ("CLM-9090", "CLAIM_REPORTED", "Reporte de siniestro de choque recibido"),
        ("CLM-9090", "TOW_TRUCK_DISPATCHED", "Grúa despachada en camino a la ubicación (Placa GRU-882)"),
        ("CLM-9090", "EXPERT_ASSESSING", "Ajustador evaluando daños en taller autorizado"),
        ("CLM-9090", "CLAIM_PAID", "Indemnización aprobada y girada a la cuenta bancaria")
    ]
}

async def generate_events():
    print("🚀 Generador de Eventos Distribuidos Kafka iniciado...", flush=True)
    await asyncio.sleep(2.0) # Esperar a que el Gateway levante

    async with httpx.AsyncClient(timeout=10.0) as client:
        step = 0
        while True:
            for category, sequence in STATUS_SEQUENCES.items():
                entity_id, status_val, detail_val = sequence[step % len(sequence)]
                payload = {
                    "event_type": category,
                    "entity_id": entity_id,
                    "status": status_val,
                    "detail": detail_val
                }

                try:
                    await client.post(GATEWAY_URL, json=payload)
                    print(f"--> Evento publicado a Gateway [{category.upper()}]: {status_val}", flush=True)
                except Exception as e:
                    print(f"⚠️ Error conectando al Realtime Gateway: {e}", flush=True)

                await asyncio.sleep(2.0)

            step += 1

if __name__ == "__main__":
    asyncio.run(generate_events())
