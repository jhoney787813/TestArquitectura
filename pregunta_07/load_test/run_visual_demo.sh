#!/usr/bin/env bash

# Script de Demostración Visual e Interactiva - Ejercicio 7 (CQRS & Mediator Pattern .NET 9)

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
    print(" ✍️ DEMO 1: EJECUCIÓN DE COMMANDS (PILA DE ESCRITURA MEDIATR .NET 9)")
    print("="*75)
    
    print("\n1. Probando Command con Payload Inválido (Monto = 0):")
    cmd_invalid = {
        "policyType": "VIDA",
        "insuredName": "Jhon (Arquitecto)",
        "insuredEmail": "jhoney7878@gmail.com",
        "amount": 0
    }
    r1 = requests.post(f"{BASE_URL}/api/v1/policies/commands/create", json=cmd_invalid)
    print(f"   Status HTTP: {r1.status_code} (ValidationBehavior -> 422 Unprocessable Entity)")
    print(f"   Body: {r1.text}")

    print("\n2. Probando Command Válido ('CreatePolicyCommand' en C# .NET 9):")
    cmd_valid = {
        "policyType": "AUTO",
        "insuredName": "Jhon E. Arquitecto Senior",
        "insuredEmail": "jhoney7878@gmail.com",
        "amount": 4500.00
    }
    r2 = requests.post(f"{BASE_URL}/api/v1/policies/commands/create", json=cmd_valid)
    print(f"   Status HTTP: {r2.status_code}")
    print(f"   Respuesta: {json.dumps(r2.json(), indent=2)}")

elif opt == "2":
    print("\n" + "="*75)
    print(" 📖 DEMO 2: EJECUCIÓN DE QUERIES (PILA DE LECTURA READ MODEL .NET 9)")
    print("="*75)
    
    # Primero crear una póliza
    r_create = requests.post(f"{BASE_URL}/api/v1/policies/commands/create", json={
        "policyType": "HOGAR",
        "insuredName": "Cliente Ejemplo",
        "insuredEmail": "cliente@seguros.com",
        "amount": 1200.00
    }).json()
    policy_id = r_create.get("policyId") or r_create.get("policy_id")
    
    print(f"\nConsultando Query 'GetPolicyByIdQuery' para ID '{policy_id}':")
    r_query = requests.get(f"{BASE_URL}/api/v1/policies/queries/{policy_id}")
    print(f" HTTP Status: {r_query.status_code}")
    print(f" Proyección Read Model (Respuesta < 2ms):")
    print(json.dumps(r_query.json(), indent=2))

elif opt == "3":
    print("\n" + "="*75)
    print(" 🔄 DEMO 3: FLUJO COMPLETO CQRS (.NET 9 MEDIATR CLEAN ARCHITECTURE)")
    print("="*75)
    
    print("\n[PASO 1] Ejecutando 'CreatePolicyCommand' en C# .NET 9:")
    r1 = requests.post(f"{BASE_URL}/api/v1/policies/commands/create", json={
        "policyType": "SALUD",
        "insuredName": "Jhon (Arquitecto de Software)",
        "insuredEmail": "jhoney7878@gmail.com",
        "amount": 8900.00
    }).json()
    pid = r1.get("policyId") or r1.get("policy_id")
    print(f" Póliza creada en .NET 9 con ID: {pid}")

    print(f"\n[PASO 2] Consultando estado previo en el Read Model ('GetPolicyByIdQuery'):")
    r2 = requests.get(f"{BASE_URL}/api/v1/policies/queries/{pid}").json()
    status_val = r2['data']['status'] if 'data' in r2 else r2.get('status')
    print(f" Estado en Read Model: {status_val}")

    print(f"\n[PASO 3] Ejecutando comando de emisión 'EmitPolicyCommand' en C# .NET 9:")
    r3 = requests.post(f"{BASE_URL}/api/v1/policies/commands/emit", json={
        "policyId": pid,
        "paymentReference": "PAY-REF-998811"
    }).json()
    status_emit = r3.get("status") or r3.get("currentStatus")
    print(f" Resultado Emisión: {status_emit} -> Póliza {pid} ahora en ACTIVE")

    print(f"\n[PASO 4] Consultando estado final actualizado en Read Model:")
    r4 = requests.get(f"{BASE_URL}/api/v1/policies/queries/{pid}").json()
    data_res = r4.get("data", r4)
    print(f" Estado Final en Read Model: {data_res.get('status')} | Referencia Pago: {data_res.get('paymentRef') or data_res.get('payment_ref')}")

EOF
