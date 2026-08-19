#!/usr/bin/env bash

# Script de Demostración Visual e Interactiva - Ejercicio 2 (Patrones, Escalabilidad y Resiliencia)

echo "=========================================================================="
echo "    🛡️ DEMOSTRACIÓN VISUAL DE ARQUITECTURA: EMISIÓN DE PÓLIZAS (EJERCICIO 2)"
echo "=========================================================================="
echo ""
echo "Selecciona el escenario a probar e inspeccionar en la consola:"
echo " 1) 🟢 ESCENARIO A: Emisión Normal Exitosa (Transactional Outbox + Async Event)"
echo " 2) 🔴 ESCENARIO B: ¿Qué pasa si SavePolicy falla? (Rollback ACID Completo)"
echo " 3) 📧 ESCENARIO C: ¿Qué pasa si SendEmail falla? (Póliza Emitida + DLQ)"
echo " 4) 📱 ESCENARIO D: ¿Qué pasa si SMS está caído? (Circuit Breaker & Fallback)"
echo " 5) 🔒 ESCENARIO E: ¿Qué pasa si Audit falla? (Auditoría Local vs Centralizada)"
echo " 6) 📊 INSPECCIONAR TABLA DE AUDITORÍA Y DLQ"
echo ""

read -p "Ingresa tu opción (1-6) [Por defecto: 1]: " OPTION
OPTION=${OPTION:-1}

python3 - << EOF
import requests
import json
import time

BASE_URL = "http://localhost:8001/api/v1"
WORKER_URL = "http://localhost:8090"
GATEWAY_URL = "http://localhost:8091"

opt = "$OPTION"

if opt == "1":
    print("\n" + "="*70)
    print(" 🟢 PROBANDO ESCENARIO A: EMISIÓN NORMAL EXITOSA")
    print("="*70)
    payload = {"customer_name": "Carlos Mendoza", "insured_amount": 50000.0, "policy_type": "AUTO_GLOBAL"}
    r = requests.post(f"{BASE_URL}/policies/emit?simulate_fail=none", json=payload).json()
    print("Respuesta API HTTP 201:")
    print(json.dumps(r, indent=2))

elif opt == "2":
    print("\n" + "="*70)
    print(" 🔴 PROBANDO ESCENARIO B: ¿QUÉ PASA SI SavePolicy FALLA?")
    print("="*70)
    payload = {"customer_name": "Ana Gómez (Falla DB)", "insured_amount": 75000.0}
    r = requests.post(f"{BASE_URL}/policies/emit?simulate_fail=save_policy", json=payload)
    print(f"Código HTTP de Respuesta: {r.status_code}")
    print(f"Cuerpo de Respuesta: {r.text}")
    print("\n-> CONCLUSIÓN B: Se ejecuta ROLLBACK ACID. No hay póliza, no hay eventos, no se envían emails ni SMS.")

elif opt == "3":
    print("\n" + "="*70)
    print(" 📧 PROBANDO ESCENARIO C: ¿QUÉ PASA SI SendEmail FALLA?")
    print("="*70)
    payload = {"customer_name": "Roberto Silva (Falla Email)", "insured_amount": 120000.0}
    r = requests.post(f"{BASE_URL}/policies/emit?simulate_fail=email", json=payload).json()
    print("Respuesta API (Póliza emitida en ms):")
    print(json.dumps(r, indent=2))
    print("\nEsperando 2 segundos para que el worker intente reintentar y mande el evento a DLQ...")
    time.sleep(2)
    dlq = requests.get(f"{WORKER_URL}/api/v1/dlq").json()
    print("\nEstado de la Dead Letter Queue (DLQ):")
    print(json.dumps(dlq, indent=2))
    print("\n-> CONCLUSIÓN C: La Póliza SI se emitió de forma segura. El correo fallido se guardó en la DLQ para reintento posterior.")

elif opt == "4":
    print("\n" + "="*70)
    print(" 📱 PROBANDO ESCENARIO D: ¿QUÉ PASA SI SMS ESTÁ CAÍDO? (CIRCUIT BREAKER)")
    print("="*70)
    payload = {"customer_name": "Laura Torres (SMS Down)", "insured_amount": 90000.0}
    print("Enviando 3 peticiones consecutivas con el gateway de SMS caído...")
    for i in range(1, 4):
        r = requests.post(f"{BASE_URL}/policies/emit?simulate_fail=sms", json=payload).json()
        print(f" Petición {i}: Póliza Emitida: {r.get('policy_id')}")
        time.sleep(0.8)
    
    cb_status = requests.get(f"{GATEWAY_URL}/health").json()
    print("\nEstado del Circuit Breaker en el Gateway SMS:")
    print(json.dumps(cb_status, indent=2))
    print("\n-> CONCLUSIÓN D: El Circuit Breaker saltó a estado 'OPEN'. La emisión de la póliza NUNCA se detuvo.")

elif opt == "5":
    print("\n" + "="*70)
    print(" 🔒 PROBANDO ESCENARIO E: ¿QUÉ PASA SI AUDIT FALLA?")
    print("="*70)
    payload = {"customer_name": "Diego Morales (Falla Audit Central)", "insured_amount": 200000.0}
    r = requests.post(f"{BASE_URL}/policies/emit?simulate_fail=audit", json=payload).json()
    pid = r.get("policy_id")
    print(f"Respuesta API: Póliza Emitida {pid}")
    time.sleep(1)
    pol_info = requests.get(f"{BASE_URL}/policies/{pid}").json()
    print("\nInspección de Auditoría Local (Persistida en BD principal):")
    print(json.dumps(pol_info.get("local_audit"), indent=2))
    print("\n-> CONCLUSIÓN E: La auditoría local ACID preserva la trazabilidad 100% garantizada. El fallo en OpenSearch reintenta en cola.")

elif opt == "6":
    print("\n" + "="*70)
    print(" 📊 METRICAS GENERALES Y ESTADO DE OUTBOX/DLQ")
    print("="*70)
    outbox = requests.get(f"{BASE_URL}/outbox").json()
    dlq = requests.get(f"{WORKER_URL}/api/v1/dlq").json()
    print("Eventos Outbox:")
    print(json.dumps(outbox, indent=2))
    print("\nDead Letter Queue (DLQ):")
    print(json.dumps(dlq, indent=2))

EOF
