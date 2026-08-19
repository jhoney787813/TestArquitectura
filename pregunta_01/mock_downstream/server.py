import time
import os
import asyncio
from fastapi import FastAPI

app = FastAPI(title="Mock Downstream Service")

DELAY_SECONDS = float(os.getenv("DELAY_SECONDS", "8.0"))

@app.get("/health")
async def health():
    return {"status": "UP"}

@app.get("/api/v1/external-data")
async def get_external_data(order_id: str = "UNKNOWN"):
    """
    Simula una dependencia externa lenta (Legacy ERP / Base de Datos sin índice / API de tercero)
    que tarda 8 segundos en responder. Mientras espera, no consume CPU (async sleep / I/O wait).
    """
    start = time.time()
    await asyncio.sleep(DELAY_SECONDS)
    elapsed = time.time() - start

    return {
        "status": "success",
        "order_id": order_id,
        "legacy_system_response_time": round(elapsed, 2),
        "payload": {
            "inventory_status": "RESERVED",
            "payment_gateway": "AUTHORIZED",
            "warehouse_id": "WH-9921"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
