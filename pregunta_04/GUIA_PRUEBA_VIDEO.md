# Guía Paso a Paso para la Grabación del Video usando la Aplicación Cliente (`http://localhost:8084`)

Esta guía te indica exactamente qué decir y qué botones presionar en pantalla para grabar una demostración perfecta e impecable del **Ejercicio 4**.

---

## 🎬 PREPARACIÓN DE PANTALLA

1. Abre tu navegador y navega a la URL del contenedor cliente dedicado:
   👉 **`http://localhost:8084`**
2. Asegúrate de tener visible la consola de salida negra en la parte inferior de la pantalla.

---

## 📹 GUÍA DE SUSTENTACIÓN PASO A PASO EN PANTALLA

### 🔹 PASO 1: Presentación e Inicio de Sesión (Pestaña 1: AUTH & REDIS REVOKED)

* **Qué decir a la cámara**:
  > *"Comenzamos en la Pestaña 1 de nuestra aplicación cliente. Aquí nos autenticamos contra el servidor OAuth 2.0 en .NET 9. Hacemos clic en '🔑 1. Iniciar Sesión'."*

* **Acción en pantalla**: Haz clic en el botón azul **"🔑 1. Iniciar Sesión (POST /api/v1/auth/login)"**.

* **Resultado a destacar**:
  > *"En la consola observamos la emisión del Access Token JWT firmado asimétricamente mediante RS256 con una validez de 15 minutos."*

---

### 🔹 PASO 2: Demostración de REST API Protegida (Pestaña 2: REST API)

* **Qué hacer**: Haz clic en la **Pestaña 2: 🌐 2. REST API**.

* **Qué decir a la cámara**:
  > *"En la Pestaña 2 probamos el recurso protegido REST API. Hacemos clic en '🚀 Probar GET /api/v1/policies'. El middleware de .NET 9 valida estatutariamente la firma RS256 del token en la cabecera Bearer y nos otorga acceso autorizado HTTP 200."*

* **Acción en pantalla**: Haz clic en el botón verde **"🚀 Probar GET /api/v1/policies"**.

* **Resultado a destacar**: En el log aparece la respuesta verde `✅ REST AUTORIZADO (HTTP 200)` mostrando las pólizas activas.

---

### 🔹 PASO 3: Demostración de SOAP API WSDL (Pestaña 3: SOAP WSDL API)

* **Qué hacer**: Haz clic en la **Pestaña 3: 🧼 3. SOAP WSDL API**.

* **Qué decir a la cámara**:
  > *"En la Pestaña 3 probamos la integración con SOAP. Vemos el Envelope XML con la cabecera WS-Security. Hacemos clic en '🧼 Invocar Servicio SOAP'. El Inspector de WCF/SoapCore extrae el token del XML y retorna la respuesta SOAP exitosa."*

* **Acciones en pantalla**:
  1. Haz clic en **"🧼 Invocar Servicio SOAP"** -> Muestra `✅ SOAP RESPUESTA EXITOSA (HTTP 200 XML)`.
  2. Haz clic en **"📄 Ver WSDL XML"** -> Muestra la estructura formal del WSDL.

---

### 🔹 PASO 4: Demostración de WebSockets en Tiempo Real (Pestaña 4: WEBSOCKETS STREAM)

* **Qué hacer**: Haz clic en la **Pestaña 4: ⚡ 4. WEBSOCKETS STREAM**.

* **Qué decir a la cámara**:
  > *"En la Pestaña 4 abrimos un canal bi-direccional en tiempo real. Hacemos clic en '🔌 Conectar WebSocket'. El Handshake valida el token y el indicador pasa a CONECTADO en verde. Enviamos marcos de datos y recibimos la confirmación instantánea."*

* **Acciones en pantalla**:
  1. Haz clic en el botón verde **"🔌 Conectar WebSocket"** -> El badge cambia a `CONECTADO` en verde.
  2. Haz clic en **"Enviar Marco"** -> Muestra el intercambio de mensajes en tiempo real.

---

### 🔹 PASO 5: LA PRUEBA REINA - Revocación de Tokens en Redis Blacklist (Pregunta B)

* **Qué decir a la cámara**:
  > *"Ahora demostramos la respuesta a la Pregunta B: ¿Cómo revocamos tokens? Hacemos clic en el botón rojo '🛑 Revocar Token en Redis'. La firma única del token (JTI) es registrada en la Redis Blacklist con un TTL. Observen los 3 efectos inmediatos:*
  > 
  > *1. El WebSocket activo en la Pestaña 4 se desconecta y expulsa en tiempo real con el código 1008 Policy Violation.*  
  > *2. Si volvemos a la Pestaña 2 (REST) y hacemos clic en Probar REST, Redis nos rechaza en sub-milisegundos con HTTP 401 TOKEN_REVOKED.*  
  > *3. Si volvemos a la Pestaña 3 (SOAP) e invocamos la operación XML, la solicitud es rechazada con un SOAP Fault HTTP 401."*

* **Acciones en pantalla**:
  1. En la Pestaña 4 o 1, haz clic en el botón rojo **"🛑 Revocar Token en Redis"**.
  2. Muestra cómo el badge de WebSocket pasa a **`DESCONECTADO`** en rojo.
  3. Cambia a la **Pestaña 2 (REST API)** y haz clic en **"🚀 Probar GET /api/v1/policies"** -> En el log aparece el rechazo rojo `🛑 REST RECHAZADO (HTTP 401): TOKEN_REVOKED`.
  4. Cambia a la **Pestaña 3 (SOAP API)** y haz clic en **"🧼 Invocar Servicio SOAP"** -> En el log aparece el rechazo rojo `🛑 SOAP RECHAZADO / FAULT (HTTP 401 XML)`.

---

## 🎯 CONCLUSIÓN PARA EL FINAL DEL VIDEO

> *"Con esto queda demostrado un esquema de seguridad unificado y estatutario para REST, SOAP y WebSockets, respaldado por un mecanismo de revocación instantánea en sub-milisegundos mediante Redis Blacklist y empaquetado en contenedores Podman. ¡Muchas gracias!"*
