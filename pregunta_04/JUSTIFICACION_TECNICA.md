# Sustentación Técnica - Ejercicio 4: Autenticación, Autorización y Revocación de Tokens

**Rol**: Arquitecto Senior de Software / Arquitecto de Soluciones  
**Metodología de Arquitectura**: **Why-Driven Design (WDD)**  
**Enfoque Central**: Clean Architecture (.NET 9), Atributos ISO/IEC 25010, Trade-offs y Modelo C4  
**Diagramas C4 para Draw.io**: [`diagrams/c4_security_architecture.drawio`](file:///Users/deals/Documents/GIT/TestArquitectura/pregunta_04/diagrams/c4_security_architecture.drawio)  
**Contenedor Cliente Dedicado**: `http://localhost:8084`  
**Proyecto de Referencia**: `pregunta_04/`  

---

## 💡 1. Explicación Didáctica y Accesible (La Analogía del Pasaporte Biométrico y la Interpol)

> **Para explicar este esquema de seguridad a cualquier audiencia:**
> 
> Imagine que viaja internacionalmente con un **Pasaporte Biométrico**:
> 
> 1. **Token JWT (RS256)**: Es su **Pasaporte Biométrico con Firma Digital**. Cualquier oficial de seguridad en cualquier puesto fronterizo (sea REST, SOAP o WebSockets) puede verificar la validez del pasaporte escaneando la **Clave Pública**, sin necesidad de llamar al país de origen a cada segundo.
> 2. **Revocación de Tokens (Redis Token Blacklist)**: Si su pasaporte es robado, la Interpol lo registra inmediatamente en la **Lista Negra Global en Tiempo Real (Redis Blacklist con TTL)**. Al intentar cruzar por cualquier puesto (REST, SOAP o WebSocket), la aduana revisa la lista negra en microsegundos y deniega el acceso (`401 Unauthorized / Token Revoked`).
> 3. **Desconexión de WebSockets en Caliente**: Si usted ya estaba dentro de la sala VIP (WebSocket activo) y su pasaporte es revocado, la seguridad del aeropuerto lo escolta fuera inmediatamente (cierre del socket en tiempo real).

---

## 🎨 2. Modelo C4 de la Arquitectura de Seguridad (C4 Level 2 - Container Diagram)

El siguiente diagrama en formato **C4 Model** representa la estructura unificada de seguridad y revocación:

```mermaid
graph TB
    subgraph Users ["1. ACTORES Y CLIENTES"]
        User["Persona: Cliente / Usuario / Aplicación<br>Autentica vía OAuth 2.0 / JWT y consume REST, SOAP y WebSockets"]
    end

    subgraph SystemBoundary ["2. C4 SYSTEM BOUNDARY: ESQUEMA DE SEGURIDAD MULTI-PROTOCOLO"]
        IdP["Container: Identity Provider & Auth Server<br>(.NET 9 Clean Architecture)<br>Emisión de Access Tokens JWT RS256"]
        
        RedisBlacklist[("Container: Redis Token Blacklist<br>(Redis Cluster TTL = Token Expiry)<br>Almacena JTIs revocados para validación instantánea en <1ms")]
        
        REST["Container: REST API Gateway<br>(Endpoints /api/v1/policies)<br>Valida Header Bearer JWT & Redis Blacklist"]
        
        SOAP["Container: SOAP WSDL Service<br>(Endpoint /soap/PolicySoapService.svc)<br>Valida WS-Security Header & Redis Blacklist"]
        
        WS["Container: WebSockets Gateway<br>(Endpoint ws://localhost:8003/ws/secure-stream)<br>Handshake de seguridad & Cierre en caliente si token se revoca"]

        ClientApp["Container: WebSocket Client UI<br>(http://localhost:8084)<br>Contenedor dedicado para pruebas interactivas"]
    end

    User -->|1. POST /login| IdP
    IdP -.->|2. JWT RS256 Token| User

    User -->|3a. REST Request (Bearer)| REST
    User -->|3b. SOAP Request (XML)| SOAP
    User -->|3c. WS Connect (Token)| WS
    ClientApp -.->|Conecta y Pruebas| WS

    IdP -->|Revoca Token JTI| RedisBlacklist
    REST -.->|Check Blacklist <1ms| RedisBlacklist
    SOAP -.->|Check Blacklist <1ms| RedisBlacklist
    WS -.->|Cierra Socket si Revocado| RedisBlacklist

    classDef c4User fill:#08427b,stroke:#073866,fontColor:#ffffff;
    classDef c4Container fill:#1168bd,stroke:#0e5296,fontColor:#ffffff;
    classDef c4Db fill:#85bbf0,stroke:#0e5296,fontColor:#000000;
    classDef c4Producer fill:#2b7bba,stroke:#0e5296,fontColor:#ffffff;

    class User c4User;
    class IdP,REST,SOAP,WS,ClientApp c4Container;
    class RedisBlacklist c4Db;
```

---

## 🎯 3. Puntos Clave que Debes Exponer en tu Presentación

Cuando estés frente al jurado evaluador o grabando tu video, estructura tu exposición en **5 puntos de alto impacto**:

1. **Arquitectura Limpia (.NET 9 Clean Architecture)**:
   Muestra que el código separa estrictamente la lógica de negocio (Dominio y Casos de Uso) de los adaptadores de entrada (REST, SOAP WSDL y WebSockets Handlers), haciendo que la seguridad sea 100% reutilizable.
2. **Firma Asimétrica JWT RS256 (Pregunta A)**:
   Explica que la autenticación es estatutaria (*stateless*). Cada API verifica la firma del JWT con la clave pública sin consultar la base de datos a cada llamada.
3. **Mecanismo de Revocación en Redis Blacklist (Pregunta B)**:
   Explica que al hacer Logout o revocación administrativa, la firma única del token (`jti`) ingresa a un clúster de **Redis con TTL igual al tiempo de vida del JWT**. Esto permite que la verificación tome **sub-milisegundos (< 1ms)**.
4. **Cierre Dinámico de WebSockets en Caliente**:
   Destaca que si un usuario tiene un socket abierto y su token es revocado, el servidor detecta el evento en Redis y **cierra la conexión WebSocket inmediatamente con código `1008 Policy Violation`**.
5. **Despliegue 100% Contenedorizado en Podman**:
   Muestra que la API corre en `security_api_p4` (Puerto 8003) y el cliente visual corre en un contenedor independiente `websocket_client_p4` en el puerto 8084 (`http://localhost:8084`).

---

## 🔍 4. Respuestas Exhaustivas a las Preguntas A y B

### A) Diseñar el Esquema de Seguridad (REST, SOAP, WebSockets)

* **Propuesta**: **OAuth 2.0 / OpenID Connect (OIDC)** con **Access Tokens JWT firmados asimétricamente mediante RS256 (RSA 2048-bit)** + **RBAC/ABAC**.
* **REST**: Cabecera `Authorization: Bearer <JWT>`. Validado por middleware .NET 9.
* **SOAP (WCF / SoapCore)**: Cabecera XML `WS-Security` (`<wsse:BinarySecurityToken>`) o HTTP Bearer Header, auditado por un Soap Inspector.
* **WebSockets**: Conexión WSS + Token Query Parameter (`wss://host/ws/secure-stream?token=<JWT>`), validado durante el handshake inicial.

### B) ¿Cómo revoca tokens?

* **Redis Token Blacklisting con TTL**: Se almacena el identificador `jti` en Redis con tiempo de vida (TTL) automatizado. Cualquier intento en REST, SOAP o WebSockets consulta Redis en < 1ms y rechaza la solicitud (`401 TOKEN_REVOKED`).
* **Short-Lived Access Tokens (15 minutos)** + **Refresh Token Rotation (RTR)**: Tokens de acceso de corta duración combinados con rotación de tokens de refresco en base de datos.
