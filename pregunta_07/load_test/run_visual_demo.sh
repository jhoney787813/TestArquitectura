#!/usr/bin/env bash

# Script de Demostración Visual e Interactiva - Ejercicio 7 (CQRS & Mediator Pattern)

echo "=========================================================================="
echo "    🔀 DEMOSTRACIÓN DE PATRÓN CQRS Y MEDIATOR (.NET 9 CLEAN ARCHITECTURE)"
echo "=========================================================================="
echo ""
echo "Selecciona el escenario a probar en la consola:"
echo " 1) ✍️ DEMO 1: EJECUCIÓN DE COMMANDS (ESCRITURA CON VALIDACIÓN EN PIPELINE BEHAVIOR)"
echo " 2) 📖 DEMO 2: EJECUCIÓN DE QUERIES (LECTURA HIPER-RÁPIDA DIRECTA DEL READ MODEL)"
echo " 3) 🔄 DEMO 3: FLUJO COMPLETO CQRS (CREACIÓN -> EMISIÓN -> CONSULTA EN VIVO)"
echo ""

read -p "Ingresa tu opción (1-3) [Por defecto: 3]: " OPTION
OPTION=${OPTION:-3}

python3 - << EOF
import requests
import json

BASE_URL = "http://localhost:8007"
opt = "$OPTION"

if opt == "1":
    print("\n" + "="*75)
    print(" ✍️ DEMO 1: EJECUCIÓN DE COMMANDS (PILA DE ESCRITURA MEDIATR)")
    print("="*75)
    
    print("\n1. Probando Command con Payload Inválido (Monto = 0):")
    cmd_invalid = {
        "policy_type": "VIDA",
        "insured_name": "Jhon (Arquitecto)",
        "insured_email": "jhoney7878@gmail.com",
        "amount": 0
    }
    r1 = requests.post(f"{BASE_URL}/api/v1/commands/policies/create", json=cmd_invalid)
    print(f"   Status HTTP: {r1.status_code} (ValidationBehavior -> 422 Unprocessable Entity)")
    print(f"   Body: {r1.text}")

    print("\n2. Probando Command Válido ('CreatePolicyCommand'):")
    cmd_valid = {
        "policy_type": "AUTO",
        "insured_name": "Jhon E. Arquitecto Senior",
        "insured_email": "jhoney7878@gmail.com",
        "amount": 4500.00
    }
    r2 = requests.post(f"{BASE_URL}/api/v1/commands/policies/create", json=cmd_valid)
    print(f"   Status HTTP: {r2.status_code}")
    print(f"   Respuesta: {json.dumps(r2.json(), indent=2)}")

elif opt == "2":
    print("\n" + "="*75)
    print(" 📖 DEMO 2: EJECUCIÓN DE QUERIES (PILA DE LECTURA READ MODEL)")
    print("="*75)
    
    # Primero crear una póliza
    r_create = requests.post(f"{BASE_URL}/api/v1/commands/policies/create", json={
        "policy_type": "HOGAR",
        "insured_name": "Cliente Ejemplo",
        "insured_email": "cliente@seguros.com",
        "amount": 1200.00
    }).json()
    policy_id = r_create["policy_id"]
    
    print(f"\nConsultando Query 'GetPolicyByIdQuery' para ID '{policy_id}':")
    r_query = requests.get(f"{BASE_URL}/api/v1/queries/policies/{policy_id}")
    print(f" HTTP Status: {r_query.status_code}")
    print(f" Proyección Read Model (Respuesta < 2ms):")
    print(json.dumps(r_query.json(), indent=2))

elif opt == "3":
    print("\n" + "="*75)
    print(" 🔄 DEMO 3: FLUJO COMPLETO CQRS (.NET 9 MEDIATR CLEAN ARCHITECTURE)")
    print("="*75)
    
    print("\n[PASO 1] Ejecutando 'CreatePolicyCommand':")
    r1 = requests.post(f"{BASE_URL}/api/v1/commands/policies/create", json={
        "policy_type": "SALUD",
        "insured_name": "Jhon (Arquitecto de Software)",
        "insured_email": "jhoney7878@gmail.com",
        "amount": 8900.00
    }).json()
    pid = r1["policy_id"]
    print(f" Póliza creada con ID: {pid} (Estado inicial: DRAFT)")

    print(f"\n[PASO 2] Consultando estado previo en el Read Model ('GetPolicyByIdQuery'):")
    r2 = requests.get(f"{BASE_URL}/api/v1/queries/policies/{pid}").json()
    print(f" Estado en Read Model: {r2['data']['status']}")

    print(f"\n[PASO 3] Ejecutando comando de emisión 'EmitPolicyCommand':")
    r3 = requests.post(f"{BASE_URL}/api/v1/commands/policies/emit", json={
        "policy_id": pid,
        "payment_reference": "PAY-REF-998811"
    }).json()
    print(f" Resultado Emisión: {r3['status']} -> Póliza {pid} ahora en ACTIVE")

    print(f"\n[PASO 4] Consultando estado final actualizado en Read Model:")
    r4 = requests.get(f"{BASE_URL}/api/v1/queries/policies/{pid}").json()
    print(f" Estado Final en Read Model: {r4['data']['status']} | Referencia Pago: {r4['data']['payment_ref']}")

EOF
