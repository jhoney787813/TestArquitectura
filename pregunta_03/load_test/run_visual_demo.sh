#!/usr/bin/env bash

# Script de Demostración Visual e Interactiva - Ejercicio 3 (Real-Time Architecture)

echo "=========================================================================="
echo "    ⚡ DEMOSTRACIÓN EN TIEMPO REAL: EMISIÓN, INSPECCIÓN Y SINIESTROS"
echo "=========================================================================="
echo ""
echo "Selecciona la tecnología en tiempo real a inspeccionar en vivo:"
echo " 1) 🟢 DEMO 1: SERVER-SENT EVENTS (SSE) - Stream HTTP/2 Push en Vivo"
echo " 2) 🟣 DEMO 2: WEBSOCKETS (Full-Duplex TCP) - Conexión Persistente"
echo " 3) 🟡 DEMO 3: SIGNALR HUB NETWORKING - Negociación de Transportes"
echo " 4) 🔴 DEMO 4: POLLING COMPARATIVE - Ineficiencia Short vs Long Polling"
echo ""

read -p "Ingresa tu opción (1-4) [Por defecto: 1]: " OPTION
OPTION=${OPTION:-1}

python3 - << EOF
import requests
import json
import time

BASE_URL = "http://localhost:8002/api/v1/realtime"
opt = "$OPTION"

if opt == "1":
    print("\n" + "="*75)
    print(" 🟢 CONECTANDO A STREAM SSE (SERVER-SENT EVENTS) EN TIEMPO REAL...")
    print(" Observa cómo llegan los eventos de Emisión, Inspección y Siniestros sin refrescar...")
    print("="*75 + "\n")
    
    try:
        response = requests.get(f"{BASE_URL}/stream", stream=True, timeout=15)
        count = 0
        for line in response.iter_lines():
            if line:
                line_str = line.decode('utf-8')
                if line_str.startswith("data: "):
                    json_data = json.loads(line_str[6:])
                    count += 1
                    cat = json_data.get("category", json_data.get("type", "SYSTEM")).upper()
                    entity = json_data.get("entity_id", "")
                    status = json_data.get("status", json_data.get("message", ""))
                    detail = json_data.get("detail", "")
                    print(f" ⚡ [EVENTO SSE #{count:02d}] Categoria: {cat:<12} | ID: {entity:<10} | Estado: {status:<22} | {detail}")
                    if count >= 8:
                        print("\n--> [STREAM SSE COMPROBADO EXITOSAMENTE]"); break
    except Exception as e:
        print(f"Error conectando a SSE: {e}")

elif opt == "2":
    print("\n" + "="*75)
    print(" 🟣 CONECTANDO A WEBSOCKETS FULL-DUPLEX...")
    print("="*75)
    print("Para probar WebSockets ejecute la transmisión usando curl/python:")
    print(f" URL: ws://localhost:8002/api/v1/realtime/ws")
    r = requests.get("http://localhost:8002/health").json()
    print("\nEstado del Servidor de WebSockets:")
    print(json.dumps(r, indent=2))

elif opt == "3":
    print("\n" + "="*75)
    print(" 🟡 CONSULTANDO SIGNALR HUB CORE NEGOTIATION & REDIS BACKPLANE")
    print("="*75)
    r = requests.get(f"{BASE_URL}/signalr-hub").json()
    print(json.dumps(r, indent=2))
    print("\n-> CONCLUSIÓN SIGNALR: Negocia WebSockets -> SSE -> Long Polling automáticamente y escala nodos mediante Redis Backplane.")

elif opt == "4":
    print("\n" + "="*75)
    print(" 🔴 COMPARACIÓN DE POLLING (SHORT POLLING vs LONG POLLING)")
    print("="*75)
    print("1. Ejecutando Short Polling (Respuesta instantánea repetitiva):")
    sp = requests.get(f"{BASE_URL}/polling?mode=short").json()
    print(json.dumps(sp, indent=2))
    
    print("\n2. Ejecutando Long Polling (Retiene conexión HTTP por 3s):")
    start = time.time()
    lp = requests.get(f"{BASE_URL}/polling?mode=long").json()
    print(f" Latencia percibida en Long Polling: {time.time()-start:.2f}s")
    print(json.dumps(lp, indent=2))

EOF
