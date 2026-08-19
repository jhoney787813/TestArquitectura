# Guía Paso a Paso para la Grabación del Video de Sustentación (Ejercicio 3)

Esta guía te explica exactamente cómo demostrar la transmisión de eventos en tiempo real (SSE, WebSockets, SignalR y Polling) para Emisión, Inspección y Siniestros.

---

## 🎬 PREPARACIÓN PREVIA DE LA TERMINAL

```bash
cd /Users/deals/Documents/GIT/TestArquitectura/pregunta_03
```

---

## 📹 GUÍA DE DEMOSTRACIÓN PASO A PASO EN LA CONSOLA

### 🔹 Paso 1: Ejecutar el Menú Interactivo de Tiempo Real
```bash
./load_test/run_visual_demo.sh
```

En la pantalla aparecerá:

```text
==========================================================================
    ⚡ DEMOSTRACIÓN EN TIEMPO REAL: EMISIÓN, INSPECCIÓN Y SINIESTROS
==========================================================================

Selecciona la tecnología en tiempo real a inspeccionar en vivo:
 1) 🟢 DEMO 1: SERVER-SENT EVENTS (SSE) - Stream HTTP/2 Push en Vivo
 2) 🟣 DEMO 2: WEBSOCKETS (Full-Duplex TCP) - Conexión Persistente
 3) 🟡 DEMO 3: SIGNALR HUB NETWORKING - Negociación de Transportes
 4) 🔴 DEMO 4: POLLING COMPARATIVE - Ineficiencia Short vs Long Polling
```

---

### 🟢 DEMO 1: STREAM SSE EN TIEMPO REAL (Push continuo sin recargar)

Ingresa `1` y presiona Enter.

**Salida en consola en vivo**:
```text
 ⚡ [EVENTO SSE #01] Categoria: EMISION      | ID: POL-1010   | Estado: POLICY_SUBMITTED       | Solicitud de póliza recibida
 ⚡ [EVENTO SSE #02] Categoria: INSPECCION   | ID: INS-5050   | Estado: INSPECTOR_ASSIGNED     | Perito asignado: Ing. Roberto
 ⚡ [EVENTO SSE #03] Categoria: SINIESTROS   | ID: CLM-9090   | Estado: TOW_TRUCK_DISPATCHED   | Grúa despachada en camino (GRU-882)
 ⚡ [EVENTO SSE #04] Categoria: EMISION      | ID: POL-1010   | Estado: POLICY_EMITTED         | Póliza emitida exitosamente
```

* **Qué decir a la cámara**:
  > *"Como vemos en la terminal, Server-Sent Events (SSE) recibe el stream continuo empujado desde Kafka sin que el navegador tenga que hacer peticiones repetitivas."*

---

### 🟡 DEMO 3: INSPECCIONAR SIGNALR HUB & REDIS BACKPLANE

Ingresa `3` y presiona Enter.

**Salida en consola**:
```json
{
  "framework": "SignalR Hub Core v8.0",
  "transport_negotiation": [
    {"transport": "WebSockets", "status": "AVAILABLE", "recommended": true},
    {"transport": "ServerSentEvents", "status": "AVAILABLE", "recommended": false},
    {"transport": "LongPolling", "status": "FALLBACK_AVAILABLE", "recommended": false}
  ],
  "redis_backplane": "ENABLED (Cluster Scale-out Across Nodes)"
}
```

* **Qué decir a la cámara**:
  > *"SignalR abstrae la negociación automática de transportes y utiliza un Redis Pub/Sub Backplane para sincronizar eventos entre múltiples nodos del Gateway."*

---

### 🔴 DEMO 4: COMPARACIÓN DE INEFICIENCIA DE POLLING

Ingresa `4` y presiona Enter.

**Salida en consola**:
```text
1. Short Polling: Retorna de inmediato (95% de peticiones sin cambios, desperdicia CPU/Red).
2. Long Polling: Mantiene la petición HTTP retenida 3.0s antes de responder.
```

---

## 🎯 RESUMEN DE COMANDOS RÁPIDOS

```bash
# 1. Ubicarse en la carpeta
cd /Users/deals/Documents/GIT/TestArquitectura/pregunta_03

# 2. Desplegar servicios en Podman
podman compose up -d --build

# 3. Lanzar la demostración interactiva
./load_test/run_visual_demo.sh
```
