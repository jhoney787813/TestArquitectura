# Guía Paso a Paso para la Grabación del Video de Sustentación (Ejercicio 2)

Esta guía explica exactamente qué comandos ejecutar y qué mostrar en pantalla para demostrar la resiliencia en la emisión de pólizas (Escenarios A, B, C, D y E).

---

## 🎬 PREPARACIÓN PREVIA DE LA TERMINAL

```bash
cd /Users/deals/Documents/GIT/TestArquitectura/pregunta_02
```

---

## 📹 GUÍA DE DEMOSTRACIÓN PASO A PASO EN LA CONSOLA

### 🔹 Paso 1: Ejecutar el Menú Interactivo de Resiliencia
```bash
./load_test/run_visual_demo.sh
```

En la pantalla aparecerá:

```text
==========================================================================
    🛡️ DEMOSTRACIÓN VISUAL DE ARQUITECTURA: EMISIÓN DE PÓLIZAS (EJERCICIO 2)
==========================================================================

Selecciona el escenario a probar e inspeccionar en la consola:
 1) 🟢 ESCENARIO A: Emisión Normal Exitosa (Transactional Outbox + Async Event)
 2) 🔴 ESCENARIO B: ¿Qué pasa si SavePolicy falla? (Rollback ACID Completo)
 3) 📧 ESCENARIO C: ¿Qué pasa si SendEmail falla? (Póliza Emitida + DLQ)
 4) 📱 ESCENARIO D: ¿Qué pasa si SMS está caído? (Circuit Breaker & Fallback)
 5) 🔒 ESCENARIO E: ¿Qué pasa si Audit falla? (Auditoría Local vs Centralizada)
 6) 📊 INSPECCIONAR TABLA DE AUDITORÍA Y DLQ
```

---

### 🟢 OPCIÓN 1: PROBAR ESCENARIO A (Emisión Exitosa < 50ms)

Ingresa `1` y presiona Enter.

**Salida en consola**:
```text
Respuesta API HTTP 201:
{
  "status": "SUCCESS",
  "message": "Policy emitted successfully",
  "policy_id": "POL-A1B2C3D4",
  "response_time_ms": 32.4,
  "note": "Notificaciones (Email/SMS) y Auditoría Centralizada se procesan asíncronamente vía Outbox."
}
```

---

### 🔴 OPCIÓN 2: PROBAR ESCENARIO B (Fallo en SavePolicy - Rollback)

Ingresa `2` y presiona Enter.

**Salida en consola**:
```text
Código HTTP de Respuesta: 500
Cuerpo de Respuesta: {"status": "ERROR", "message": "SavePolicy failed. Transaction rolled back completely.", "policy_created": false}

-> CONCLUSIÓN B: Se ejecuta ROLLBACK ACID. No hay póliza, no hay eventos, no se envían emails ni SMS.
```

---

### 📧 OPCIÓN 3: PROBAR ESCENARIO C (Fallo en SendEmail - Póliza Guardada + DLQ)

Ingresa `3` y presiona Enter.

**Salida en consola**:
```text
Respuesta API (Póliza emitida en ms): POL-EMAIL123
Estado de la Dead Letter Queue (DLQ):
{
  "dlq_total": 1,
  "messages": [
    {
      "channel": "EMAIL",
      "policy_id": "POL-EMAIL123",
      "reason": "Max retries (2) exceeded or Circuit Breaker Open"
    }
  ]
}
-> CONCLUSIÓN C: La Póliza SI se emitió de forma segura. El correo fallido se guardó en la DLQ para reintento posterior.
```

---

### 📱 OPCIÓN 4: PROBAR ESCENARIO D (SMS Caído - Circuit Breaker)

Ingresa `4` y presiona Enter.

**Salida en consola**:
```text
Estado del Circuit Breaker en el Gateway SMS:
{
  "status": "UP",
  "sms_circuit_breaker": {
    "failures": 2,
    "state": "OPEN"
  }
}
-> CONCLUSIÓN D: El Circuit Breaker saltó a estado 'OPEN'. La emisión de la póliza NUNCA se detuvo.
```

---

### 🔒 OPCIÓN 5: PROBAR ESCENARIO E (Fallo en Audit Service Central)

Ingresa `5` y presiona Enter.

**Salida en consola**:
```text
Inspección de Auditoría Local (Persistida en BD principal):
[
  {
    "action": "POLICY_EMITTED_LOCAL",
    "detail": "Póliza POL-AUDIT123 emitida y persistida en BD local."
  }
]
-> CONCLUSIÓN E: La auditoría local ACID preserva la trazabilidad 100% garantizada. El fallo en OpenSearch reintenta en cola.
```

---

## 🎯 RESUMEN DE COMANDOS RÁPIDOS PARA COPIAR Y PEGAR

```bash
# 1. Ubicarse en carpeta del ejercicio
cd /Users/deals/Documents/GIT/TestArquitectura/pregunta_02

# 2. Desplegar en Podman
podman compose up -d --build

# 3. Lanzar script interactivo visual
./load_test/run_visual_demo.sh
```
