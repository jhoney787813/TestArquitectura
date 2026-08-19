import os
import asyncio
import time
import json
import uuid
import jwt
from typing import List, Dict, Optional
from datetime import datetime, timedelta
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Response, Request, Header, Query, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

app = FastAPI(
    title="Security & Auth API - Ejercicio 4 (Clean Architecture REST, SOAP & WebSockets)",
    description="Esquema de seguridad unificado con OAuth 2.0 / JWT y revocación en tiempo real mediante Redis Token Blacklist.",
    version="4.0.0"
)

# 🌐 HABILITAR CORS PARA PERMITIR PETICIONES DESDE http://localhost:8084 Y CUALQUIER ORIGEN
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuración de Seguridad y JWT
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "SuperSecretArchitectureKeyForJwtSigning2026!#$")
JWT_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15

# Simulación de Redis Token Blacklist (Store en memoria / Redis Client)
redis_token_blacklist: Dict[str, float] = {} # {jti/token: expiry_timestamp}
users_db = {
    "admin@seguros.com": {"password": "Password123!", "role": "ADMIN", "name": "Jhon (Arquitecto)"},
    "user@seguros.com": {"password": "UserPass123!", "role": "USER", "name": "Carlos Mendoza"}
}
active_websocket_connections: List[Dict] = []

# Colores ANSI para logs visuales en consola
COLOR_CYAN = "\033[96m"
COLOR_YELLOW = "\033[93m"
COLOR_GREEN = "\033[92m"
COLOR_RED = "\033[91m"
COLOR_MAGENTA = "\033[95m"
COLOR_BOLD = "\033[1m"
COLOR_RESET = "\033[0m"

# DTOs y Modelos de Dominio
class LoginRequest(BaseModel):
    username: str
    password: str

class RevokeTokenRequest(BaseModel):
    token: str
    reason: str = "LOGOUT_USER"

# ==============================================================================
# 🏛️ CAPA DE APLICACIÓN: SERVICIO DE AUTENTICACIÓN Y REVOCACIÓN EN REDIS
# ==============================================================================
class TokenBlacklistService:
    @staticmethod
    def revoke(token_jti: str, expires_in_seconds: int = 900):
        expiry = time.time() + expires_in_seconds
        redis_token_blacklist[token_jti] = expiry
        now_str = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        print(f"{COLOR_RED}[{now_str}] 🛑 [REDIS BLACKLIST] Token {token_jti[:12]}... agregado a la Lista Negra de Revocación (TTL: {expires_in_seconds}s){COLOR_RESET}", flush=True)

    @staticmethod
    def is_revoked(token_jti: str) -> bool:
        if token_jti in redis_token_blacklist:
            if time.time() < redis_token_blacklist[token_jti]:
                return True
            else:
                del redis_token_blacklist[token_jti]
        return False

class JwtSecurityService:
    @staticmethod
    def create_token(data: dict) -> str:
        to_encode = data.copy()
        jti = str(uuid.uuid4())
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"jti": jti, "exp": expire, "iss": "AuthServer.Seguros", "aud": "CoreServices"})
        return jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)

    @staticmethod
    def verify_token(token: str) -> dict:
        try:
            payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM], audience="CoreServices")
            jti = payload.get("jti")
            if TokenBlacklistService.is_revoked(jti) or TokenBlacklistService.is_revoked(token):
                raise HTTPException(status_code=401, detail="TOKEN_REVOKED: Token in Redis Blacklist")
            return payload
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="TOKEN_EXPIRED: Access Token Signature Expired")
        except jwt.PyJWTError as e:
            raise HTTPException(status_code=401, detail=f"TOKEN_INVALID: {str(e)}")

# Dependency para validar Auth Header en REST
def get_current_user(authorization: Optional[str] = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="MISSING_BEARER_TOKEN")
    token = authorization.split(" ")[1]
    return JwtSecurityService.verify_token(token)


# ==============================================================================
# 🌐 CAPA DE PRESENTACIÓN 1: REST API (Authentication & Revocation)
# ==============================================================================
@app.get("/health")
async def health():
    return {
        "status": "UP",
        "revoked_tokens_count": len(redis_token_blacklist),
        "active_websockets_count": len(active_websocket_connections)
    }

@app.post("/api/v1/auth/login")
async def login(request: LoginRequest):
    now_str = datetime.now().strftime("%H:%M:%S.%f")[:-3]
    user = users_db.get(request.username)
    if not user or user["password"] != request.password:
        print(f"{COLOR_RED}[{now_str}] ❌ [LOGIN FALLIDO] Intento fallido para usuario: {request.username}{COLOR_RESET}", flush=True)
        raise HTTPException(status_code=401, detail="INVALID_CREDENTIALS")

    token = JwtSecurityService.create_token({"sub": request.username, "role": user["role"], "name": user["name"]})
    print(f"{COLOR_GREEN}[{now_str}] 🔑 [LOGIN EXITOSO] JWT Emitido para: {request.username} (Rol: {user['role']}){COLOR_RESET}", flush=True)

    return {
        "status": "SUCCESS",
        "access_token": token,
        "token_type": "Bearer",
        "expires_in_minutes": ACCESS_TOKEN_EXPIRE_MINUTES,
        "user": {"username": request.username, "role": user["role"], "name": user["name"]}
    }

# 🔴 PREGUNTA B: REVOCACIÓN DE TOKENS
@app.post("/api/v1/auth/revoke")
async def revoke_token(request: RevokeTokenRequest):
    try:
        payload = jwt.decode(request.token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM], options={"verify_signature": True, "verify_exp": False}, audience="CoreServices")
        jti = payload.get("jti", request.token)
    except Exception:
        jti = request.token

    TokenBlacklistService.revoke(jti, expires_in_seconds=900)

    # Desconectar sockets activos que usen este token revocado
    now_str = datetime.now().strftime("%H:%M:%S.%f")[:-3]
    disconnected = 0
    for item in list(active_websocket_connections):
        if item["jti"] == jti or item["token"] == request.token:
            try:
                await item["ws"].close(code=1008, reason="TOKEN_REVOKED")
                active_websocket_connections.remove(item)
                disconnected += 1
                print(f"{COLOR_RED}[{now_str}] ⚡ [WEBSOCKET DESCONECTADO] Conexión cerrada en tiempo real por revocación de token.{COLOR_RESET}", flush=True)
            except Exception:
                pass

    return {
        "status": "REVOKED",
        "token_jti": jti,
        "reason": request.reason,
        "websockets_disconnected": disconnected,
        "message": "Token added to Redis Blacklist successfully."
    }

@app.get("/api/v1/policies")
async def get_protected_policies(current_user: dict = Depends(get_current_user)):
    now_str = datetime.now().strftime("%H:%M:%S.%f")[:-3]
    print(f"{COLOR_CYAN}[{now_str}] 🔓 [RECURSO REST PROTEGIDO] Acceso concedido a: {current_user['sub']}{COLOR_RESET}", flush=True)
    return {
        "status": "AUTHORIZED",
        "user": current_user["sub"],
        "policies": [
            {"policy_id": "POL-9901", "type": "VIDA", "status": "ACTIVE"},
            {"policy_id": "POL-9902", "type": "AUTO", "status": "ACTIVE"}
        ]
    }


# ==============================================================================
# 🧼 CAPA DE PRESENTACIÓN 2: SOAP API (WS-Security / WSDL Endpoint)
# ==============================================================================
@app.get("/soap/PolicySoapService.svc")
async def get_soap_wsdl(wsdl: Optional[str] = Query(None)):
    wsdl_xml = """<?xml version="1.0" encoding="UTF-8"?>
<wsdl:definitions name="PolicySoapService" targetNamespace="http://seguros.com/soap" xmlns:wsdl="http://schemas.xmlsoap.org/wsdl/" xmlns:tns="http://seguros.com/soap" xmlns:soap="http://schemas.xmlsoap.org/wsdl/soap/">
  <wsdl:message name="GetPolicyRequest"><wsdl:part name="PolicyId" type="xsd:string"/></wsdl:message>
  <wsdl:message name="GetPolicyResponse"><wsdl:part name="Status" type="xsd:string"/></wsdl:message>
  <wsdl:portType name="PolicySoapPort">
    <wsdl:operation name="GetPolicy"><wsdl:input message="tns:GetPolicyRequest"/><wsdl:output message="tns:GetPolicyResponse"/></wsdl:operation>
  </wsdl:portType>
  <wsdl:binding name="PolicySoapBinding" type="tns:PolicySoapPort">
    <soap:binding style="document" transport="http://schemas.xmlsoap.org/soap/http"/>
  </wsdl:binding>
</wsdl:definitions>"""
    return Response(content=wsdl_xml, media_type="application/xml")

@app.post("/soap/PolicySoapService.svc")
async def handle_soap_request(request: Request):
    body_bytes = await request.body()
    body_text = body_bytes.decode('utf-8', errors='ignore')
    now_str = datetime.now().strftime("%H:%M:%S.%f")[:-3]

    print(f"\n{COLOR_YELLOW}[{now_str}] 🧼 [PETICIÓN SOAP RECIBIDA] Procesando Envelope XML...{COLOR_RESET}", flush=True)

    # Extraer Token del Header WS-Security o Authorization Header
    auth_header = request.headers.get("Authorization", "")
    token = None
    if auth_header.startswith("Bearer "):
        token = auth_header.split(" ")[1]
    elif "<wsse:BinarySecurityToken>" in body_text:
        try:
            token = body_text.split("<wsse:BinarySecurityToken>")[1].split("</wsse:BinarySecurityToken>")[0].strip()
        except Exception:
            token = None

    if not token:
        print(f"{COLOR_RED}[{now_str}] ❌ [SOAP RECHAZADO] Token Bearer / WS-Security no encontrado en Envelope XML{COLOR_RESET}", flush=True)
        fault_xml = """<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/"><s:Body><s:Fault><faultcode>s:MustUnderstand</faultcode><faultstring>SOAP_AUTH_FAILED: Missing WS-Security Bearer Token</faultstring></s:Fault></s:Body></s:Envelope>"""
        return Response(content=fault_xml, status_code=401, media_type="application/xml")

    # Validar Firma JWT y Redis Blacklist
    try:
        user = JwtSecurityService.verify_token(token)
        print(f"{COLOR_GREEN}[{now_str}] ✅ [SOAP AUTORIZADO] Usuario: {user['sub']} validado en SOAP WSDL Service.{COLOR_RESET}", flush=True)
        response_xml = f"""<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/"><s:Body><GetPolicyResponse xmlns="http://seguros.com/soap"><Status>SUCCESS</Status><PolicyId>POL-SOAP-8801</PolicyId><Insured>{user['name']}</Insured></GetPolicyResponse></s:Body></s:Envelope>"""
        return Response(content=response_xml, status_code=200, media_type="application/xml")
    except Exception as e:
        print(f"{COLOR_RED}[{now_str}] ❌ [SOAP RECHAZADO] Token Inválido o Revocado en Redis: {e}{COLOR_RESET}", flush=True)
        fault_xml = f"""<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/"><s:Body><s:Fault><faultcode>s:Client</faultcode><faultstring>SOAP_SECURITY_ERROR: Token Revoked or Invalid ({str(e)})</faultstring></s:Fault></s:Body></s:Envelope>"""
        return Response(content=fault_xml, status_code=401, media_type="application/xml")


# ==============================================================================
# ⚡ CAPA DE PRESENTACIÓN 3: WEBSOCKETS CON SEGURIDAD Y DESCONEXIÓN EN CALIENTE
# ==============================================================================
@app.websocket("/ws/secure-stream")
async def websocket_auth_endpoint(websocket: WebSocket, token: Optional[str] = Query(None)):
    now_str = datetime.now().strftime("%H:%M:%S.%f")[:-3]
    if not token:
        print(f"{COLOR_RED}[{now_str}] ⚡ [WEBSOCKET RECHAZADO] Intento de conexión sin Token Query Param.{COLOR_RESET}", flush=True)
        await websocket.close(code=1008, reason="MISSING_TOKEN")
        return

    try:
        payload = JwtSecurityService.verify_token(token)
        jti = payload.get("jti")
        await websocket.accept()
        conn_info = {"ws": websocket, "jti": jti, "token": token, "user": payload["sub"]}
        active_websocket_connections.append(conn_info)
        print(f"{COLOR_MAGENTA}[{now_str}] 🔌 [WEBSOCKET CONECTADO] Handshake exitoso para: {payload['sub']} (JTI: {jti[:8]}){COLOR_RESET}", flush=True)

        await websocket.send_text(json.dumps({"type": "CONNECTED", "message": "Autenticado en WebSocket", "user": payload["sub"]}))

        while True:
            # Monitorear activamente la revocación del token en Redis
            if TokenBlacklistService.is_revoked(jti):
                print(f"{COLOR_RED}[{now_str}] 🛑 [WEBSOCKET EXPULSADO] Se detectó revocación en Redis del Token JTI {jti[:8]}. Cerrando socket...{COLOR_RESET}", flush=True)
                await websocket.close(code=1008, reason="TOKEN_REVOKED_IN_REDIS")
                break

            msg = await websocket.receive_text()
            await websocket.send_text(json.dumps({"type": "FRAME_ACK", "data_received": msg, "timestamp": datetime.now().isoformat()}))
    except WebSocketDisconnect:
        print(f"{COLOR_YELLOW}⚠️ WebSocket cliente desconectado.{COLOR_RESET}", flush=True)
    except Exception as e:
        print(f"{COLOR_RED}❌ Error de autenticación en WebSocket: {e}{COLOR_RESET}", flush=True)
        try:
            await websocket.close(code=1008, reason="UNAUTHORIZED")
        except Exception:
            pass
    finally:
        for item in list(active_websocket_connections):
            if item["ws"] == websocket:
                active_websocket_connections.remove(item)


# 🖥️ CLIENTE WEBSOCKET INTERACTIVO EN HTML/JS
@app.get("/client", response_class=HTMLResponse)
async def get_client_page():
    with open("/app/client/websocket_client.html", "r", encoding="utf-8") as f:
        return f.read()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
