#!/usr/bin/env bash

# Script de Demostración Visual e Interactiva - Ejercicio 5 (Observability & Exception Handling)

echo "=========================================================================="
echo "    📊 DEMOSTRACIÓN DE OBSERVABILIDAD, MODELO DE RICHARDSON Y OPENTELEMETRY"
echo "=========================================================================="
echo ""
echo "Selecciona el escenario a probar en la consola:"
echo " 1) 🔴 DEMO 1: DIAGNÓSTICO DEL ANTIPATRÓN catch(Exception ex) { return BadRequest(); }"
echo " 2) 🟢 DEMO 2: SOLUCIÓN TÉCNICA CON MAPEO DE RICHARDSON & RFC 7807 (HTTP 404, 409, 422, 503)"
echo " 3) 🔍 DEMO 3: TRAZABILIDAD DISTRIBUIDA OPENTELEMETRY (Header W3C traceparent & TraceId)"
echo " 4) 📈 DEMO 4: EXPORTADOR DE MÉTRICAS PROMETHEUS (/metrics)"
echo ""

read -p "Ingresa tu opción (1-4) [Por defecto: 2]: " OPTION
OPTION=${OPTION:-2}

python3 - << EOF
import requests
import json

BASE_URL = "http://localhost:8005"
opt = "$OPTION"

if opt == "1":
    print("\n" + "="*75)
    print(" 🔴 DEMOSTRACIÓN DEL ANTIPATRÓN: catch(Exception ex) { return BadRequest(); }")
    print(" Observa cómo todo error responde 400 BadRequest genérico sin trazas ni códigos semánticos...")
    print("="*75)
    
    print("\n1. Petición por recurso inexistente ('not-found'):")
    r1 = requests.get(f"{BASE_URL}/api/v1/bad-practice/policies/not-found")
    print(f"   Status HTTP: {r1.status_code} (¡Debería ser 404 Not Found!)")
    print(f"   Body: {r1.text}")

    print("\n2. Petición con falla de Base de Datos ('db-error'):")
    r2 = requests.get(f"{BASE_URL}/api/v1/bad-practice/policies/db-error")
    print(f"   Status HTTP: {r2.status_code} (¡Debería ser 503 Service Unavailable!)")
    print(f"   Body: {r2.text}")
    
    print("\n--> CONCLUSIÓN PREGUNTA A: catch(Exception ex) enmascara el origen real del fallo, borra las trazas y destruye el significado del protocolo HTTP.")

elif opt == "2":
    print("\n" + "="*75)
    print(" 🟢 SOLUCIÓN TÉCNICA: MAPEO DE RICHARDSON & RFC 7807 (PROBLEM DETAILS)")
    print("="*75)
    
    scenarios = [
        ("not-found", "Recurso no encontrado", 404),
        ("rule-error", "Violación de Regla de Negocio / Dominio", 422),
        ("conflict", "Conflicto de Estado Concurrente", 409),
        ("db-error", "Falla Técnica Downstream / Base de Datos", 503),
        ("unhandled", "Excepción no controlada", 500)
    ]
    
    for path_arg, desc, expected_status in scenarios:
        print(f"\nProbando escenario '{desc}' ({path_arg}):")
        r = requests.get(f"{BASE_URL}/api/v1/good-practice/policies/{path_arg}")
        print(f" HTTP Status: {r.status_code} | Content-Type: {r.headers.get('Content-Type')}")
        print(f" Header TraceId: {r.headers.get('X-Trace-ID')}")
        print(" ProblemDetails RFC 7807 JSON:")
        print(json.dumps(r.json(), indent=2))
        print("-" * 50)

elif opt == "3":
    print("\n" + "="*75)
    print(" 🔍 TRAZABILIDAD DISTRIBUIDA OPENTELEMETRY (W3C TRACEPARENT)")
    print("="*75)
    custom_traceparent = "00-4bf92f3577b34da6a3ce929d0e0e4736-00f067aa0ba902b7-01"
    headers = {"traceparent": custom_traceparent}
    print(f"Enviando cabecera W3C traceparent entrante: {custom_traceparent}")
    r = requests.get(f"{BASE_URL}/api/v1/good-practice/policies/POL-8811", headers=headers)
    print(f"Respuesta HTTP Status: {r.status_code}")
    print(f"TraceParent devuelto en respuesta: {r.headers.get('traceparent')}")
    print(f"Trace-ID extraído: {r.headers.get('X-Trace-ID')}")

elif opt == "4":
    print("\n" + "="*75)
    print(" 📈 EXPORTADOR DE MÉTRICAS PROMETHEUS (GET /metrics)")
    print("="*75)
    r = requests.get(f"{BASE_URL}/metrics")
    print(r.text)

EOF
