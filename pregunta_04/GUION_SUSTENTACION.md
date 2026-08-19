# Guión de Sustentación para Cámara - Ejercicio 4: Autenticación, Autorización y Revocación

**Formato**: Guión para video de presentación / Entrevista técnica en vivo  
**Rol**: Arquitecto Senior de Software  
**Enfoque**: Metodología **Why-Driven Design (WDD)**, Clean Architecture en .NET 9, Modelo C4 y Atributos ISO 25010  
**Duración Estimada**: 4 a 5 minutos  

---

## 🎬 ESCENA 1: MARCO METODOLÓGICO Y LA ANALOGÍA DEL PASAPORTE (0:00 - 1:00)

**[Mirada directa a la cámara, postura firme, clara y profesional]**

> **"Hola a todos.**
> 
> Abordamos el **Ejercicio 4: Autenticación, Autorización Multi-Protocolo (REST, SOAP, WebSockets) y Revocación de Tokens**.
> 
> Para entender este diseño de seguridad de forma muy didáctica, utilicemos la **analogía del Pasaporte Biométrico y la Interpol**:
> 
> - **El Token JWT (RS256)** es tu **Pasaporte Biométrico con Firma Digital**. Cualquier puesto de control (sea una API REST, un servicio SOAP o un WebSocket) puede verificar la validez del pasaporte escaneando la **Clave Pública**, sin consultar al país de origen a cada segundo.
> - **La Revocación en Redis Blacklist (Pregunta B)** es la **Lista Negra de la Interpol**. Si reportas tu pasaporte robado, la Interpol lo añade a una lista en tiempo real. Al intentar usarlo en cualquier puerta, la aduana revisa la lista en menos de un milisegundo y rechaza el ingreso.
> - **Si ya estabas dentro de la sala VIP (WebSocket activo)**, la seguridad del aeropuerto te desconecta e invalida la sesión inmediatamente."

---

## 🔍 ESCENA 2: RESPUESTA WDD A LAS PREGUNTAS A Y B (1:00 - 2:45)

**[Tono estructurado, transmitiendo seguridad y rigor de arquitectura]**

> **"Respondamos a las preguntas de la evaluación:**
> 
> **A) Esquema de Seguridad Unificado (REST, SOAP, WebSockets):**
> Diseñamos una arquitectura basada en **OAuth 2.0 / OpenID Connect con Tokens JWT firmados asimétricamente mediante RS256**.
> - **REST** transporta el token en el Header `Authorization: Bearer`.
> - **SOAP (WCF / SoapCore)** valida la cabecera XML `WS-Security` (`BinarySecurityToken`) o Bearer Header mediante un Soap Inspector.
> - **WebSockets** valida el token durante el handshake inicial WSS.
> 
> **B) Revocación de Tokens:**
> Implementamos un esquema de **Redis Token Blacklisting con TTL**. Al hacer Logout o Revocación administrativa (`POST /api/v1/auth/revoke`), se guarda el `jti` (JWT ID) en Redis. Cada API consulta Redis en < 1ms. Si el token está en la lista negra, se rechaza inmediatamente (`401 Unauthorized / Token Revoked`)."

---

## 💻 ESCENA 3: DEMOSTRACIÓN PRÁCTICA EN CONTENEDORES PODMAN (2:45 - 4:00)

**[Mostrar en pantalla la terminal y el cliente web en puerto 8084]**

> **"Para respaldar esto con una prueba práctica real en Podman:**
> 
> 1. He desplegado dos contenedores OCI independientes: `security_api_p4` en el puerto 8003 y un **Contenedor Dedicado del Cliente WebSocket** en el puerto 8084 (`http://localhost:8084`).
> 2. Al abrir `http://localhost:8084` en el navegador, iniciamos sesión REST, nos conectamos al WebSocket en vivo y presionamos **'Revocar Token en Redis'**.
> 3. En pantalla observamos cómo el servidor expulsa y desconecta el socket en tiempo real con el código `1008 Policy Violation`."

---

## 🎯 ESCENA 4: CONCLUSIÓN Y CIERRE (4:00 - 4:30)

> **"En conclusión: unificar la seguridad bajo JWT RS256 con revocación en tiempo real en Redis garantiza la máxima protección y velocidad de respuesta para REST, SOAP y WebSockets.**
> 
> Todo el código en .NET 9 Clean Architecture, el contenedor de cliente en puerto 8084, los diagramas C4 Model para Draw.io y los scripts de prueba están listos en la carpeta `pregunta_04/`. ¡Muchas gracias!"**
