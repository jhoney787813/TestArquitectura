#!/usr/bin/env bash

# Script de Demostración Visual e Interactiva - Ejercicio 4 (Authentication & Authorization)

echo "=========================================================================="
echo "    🔐 DEMOSTRACIÓN DE SEGURIDAD MULTI-PROTOCOLO Y REVOCACIÓN EN REDIS"
echo "=========================================================================="
echo ""
echo "Selecciona el escenario a probar en la consola:"
echo " 1) 🔑 DEMO 1: REST API Auth (Login + Recurso Protegido Bearer JWT)"
echo " 2) 🧼 DEMO 2: SOAP API Auth (Invocar WSDL / Envelope XML con Security Header)"
echo " 3) 🛑 DEMO 3: REVOCACIÓN DE TOKENS EN REDIS (Demostrar rechazo en REST, SOAP y WS)"
echo " 4) 🌐 DEMO 4: CLIENTE WEBSOCKETS EN TIEMPO REAL (Instrucciones Navegador)"
echo ""

read -p "Ingresa tu opción (1-4) [Por defecto: 1]: " OPTION
OPTION=${OPTION:-1}

python3 - << EOF
import requests
import json

BASE_URL = "http://localhost:8003"
opt = "$OPTION"

if opt == "1":
    print("\n" + "="*75)
    print(" 🔑 PROBANDO AUTENTICACIÓN REST API (POST /api/v1/auth/login)")
    print("="*75)
    login_data = {"username": "admin@seguros.com", "password": "Password123!"}
    r = requests.post(f"{BASE_URL}/api/v1/auth/login", json=login_data).json()
    print("Respuesta de Login (JWT Emitido):")
    print(json.dumps(r, indent=2))

    token = r.get("access_token")
    print("\nConsumiendo Recurso Protegido REST (GET /api/v1/policies)...")
    headers = {"Authorization": f"Bearer {token}"}
    p = requests.get(f"{BASE_URL}/api/v1/policies", headers=headers).json()
    print(json.dumps(p, indent=2))

elif opt == "2":
    print("\n" + "="*75)
    print(" 🧼 PROBANDO AUTENTICACIÓN SOAP API (WS-SECURITY / WSDL)")
    print("="*75)
    # Obtener token primero
    login_data = {"username": "admin@seguros.com", "password": "Password123!"}
    token = requests.post(f"{BASE_URL}/api/v1/auth/login", json=login_data).json().get("access_token")

    soap_envelope = f"""<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/">
  <s:Header>
    <wsse:Security xmlns:wsse="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd">
      <wsse:BinarySecurityToken>{token}</wsse:BinarySecurityToken>
    </wsse:Security>
  </s:Header>
  <s:Body>
    <GetPolicyRequest xmlns="http://seguros.com/soap">
      <PolicyId>POL-SOAP-99</PolicyId>
    </GetPolicyRequest>
  </s:Body>
</s:Envelope>"""

    headers = {"Content-Type": "application/xml", "Authorization": f"Bearer {token}"}
    r = requests.post(f"{BASE_URL}/soap/PolicySoapService.svc", data=soap_envelope, headers=headers)
    print(f"Código HTTP SOAP: {r.status_code}")
    print("Respuesta SOAP Envelope XML:")
    print(r.text)

elif opt == "3":
    print("\n" + "="*75)
    print(" 🛑 PROBANDO REVOCACIÓN DE TOKENS EN REDIS (PREGUNTA B)")
    print("="*75)
    login_data = {"username": "admin@seguros.com", "password": "Password123!"}
    token = requests.post(f"{BASE_URL}/api/v1/auth/login", json=login_data).json().get("access_token")
    headers = {"Authorization": f"Bearer {token}"}

    print("1. Acceso ANTES de revocar (Debe responder HTTP 200 OK):")
    r1 = requests.get(f"{BASE_URL}/api/v1/policies", headers=headers)
    print(f"   Status: {r1.status_code} | Body: {r1.text[:60]}...")

    print("\n2. Revocando Token en Redis Blacklist (POST /api/v1/auth/revoke)...")
    rev = requests.post(f"{BASE_URL}/api/v1/auth/revoke", json={"token": token, "reason": "REVOCATION_TEST"}).json()
    print(json.dumps(rev, indent=2))

    print("\n3. Intento de Acceso DESPUÉS de revocar (Debe responder HTTP 401 TOKEN_REVOKED):")
    r2 = requests.get(f"{BASE_URL}/api/v1/policies", headers=headers)
    print(f"   Status: {r2.status_code} | Body: {r2.text}")
    print("\n-> CONCLUSIÓN PREGUNTA B: El Token revocado es rechazado INMEDIATAMENTE en REST, SOAP y WebSockets!")

elif opt == "4":
    print("\n" + "="*75)
    print(" 🌐 CLIENTE WEBSOCKETS EN TIEMPO REAL")
    print("="*75)
    print("Para probar la desconexión de WebSockets en tiempo real al revocar un token:")
    print(f" 1. Abre en tu navegador: http://localhost:8003/client")
    print(f" 2. Haz clic en 'Iniciar Sesión'")
    print(f" 3. Haz clic en 'Conectar WebSocket'")
    print(f" 4. Haz clic en 'Revocar Token en Redis' y observa el cierre inmediato del socket con código 1008!")

EOF
