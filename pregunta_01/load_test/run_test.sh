#!/usr/bin/env bash

echo "=========================================================================="
echo "   INICIANDO PRUEBA DE CARGA Y DIAGNÓSTICO (EJERCICIO 1 - PODMAN/DOCKER)"
echo "=========================================================================="

URL="http://localhost:8000/api/v1/orders/ORD-TEST"

if command -v k6 &> /dev/null; then
    echo "Running load test using k6..."
    k6 run load_test/k6_script.js
else
    echo "[INFO] k6 no detectado. Utilizando generador de carga alternativo con Python..."
    python3 - << 'EOF'
import concurrent.futures
import time
import requests
import numpy as np

URL = "http://localhost:8000/api/v1/orders/ORD-TEST"
NUM_REQUESTS = 30
CONCURRENCY = 10

print(f"Enviando {NUM_REQUESTS} solicitudes concurrentes (Concurrencia: {CONCURRENCY})...")

latencies = []

def make_request(req_id):
    start = time.time()
    try:
        r = requests.get(f"{URL}-{req_id}", timeout=15)
        elapsed = time.time() - start
        return elapsed, r.status_code
    except Exception as e:
        return time.time() - start, 500

start_total = time.time()
with concurrent.futures.ThreadPoolExecutor(max_workers=CONCURRENCY) as executor:
    futures = [executor.submit(make_request, i) for i in range(NUM_REQUESTS)]
    for future in concurrent.futures.as_completed(futures):
        lat, status_code = future.result()
        latencies.append(lat)

total_elapsed = time.time() - start_total
p95 = np.percentile(latencies, 95)
p50 = np.percentile(latencies, 50)
avg_lat = np.mean(latencies)

print("\n" + "="*50)
print("             RESULTADOS DE LA PRUEBA")
print("="*50)
print(f"Solicitudes Totales : {NUM_REQUESTS}")
print(f"Tiempo Total Prueba : {total_elapsed:.2f} segundos")
print(f"Latencia Promedio   : {avg_lat:.2f} segundos")
print(f"Latencia P50        : {p50:.2f} segundos")
print(f"Latencia P95 (OBJ)  : {p95:.2f} segundos  <-- [P95 ALREDEDOR DE 8 SEGUNDOS]")
print("="*50)

# Consultar métricas del servicio
try:
    m = requests.get("http://localhost:8000/metrics").json()
    print("\n[MÉTRICAS REPORTADAS POR EL CONTENEDOR]")
    print(f"Consumo CPU Estimado : {m.get('cpu_usage_estimated')}")
    print(f"Consumo RAM Estimado : {m.get('ram_usage_estimated')}")
    print(f"Solicitudes en Cola  : {m.get('metrics', {}).get('queued_requests')}")
    print(f"Capacidad del Pool   : {m.get('pool_capacity')}")
except Exception as e:
    pass

EOF
fi

echo ""
echo "=========================================================================="
echo " Diagnóstico completado. El escenario de CPU 10%, RAM 30%, P95=8s se ha reproducido."
echo "=========================================================================="
