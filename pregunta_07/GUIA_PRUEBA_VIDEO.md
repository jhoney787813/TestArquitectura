# Guía Paso a Paso para la Grabación del Video de Sustentación (Ejercicio 7)

Esta guía explica exactamente qué comandos ejecutar y qué mostrar en pantalla para demostrar la arquitectura CQRS y el Patrón Mediator (.NET 9 Clean Architecture).

---

## 🎬 PREPARACIÓN PREVIA DE LA TERMINAL

```bash
cd /Users/deals/Documents/GIT/TestArquitectura/pregunta_07
```

---

## 📹 GUÍA DE DEMOSTRACIÓN PASO A PASO EN LA CONSOLA

### 🔹 Paso 1: Ejecutar el Menú Interactivo de CQRS
```bash
./load_test/run_visual_demo.sh
```

En la pantalla aparecerá:

```text
==========================================================================
    🔀 DEMOSTRACIÓN DE PATRÓN CQRS Y MEDIATOR (.NET 9 CLEAN ARCHITECTURE)
==========================================================================

Selecciona el escenario a probar en la consola:
 1) ✍️ DEMO 1: EJECUCIÓN DE COMMANDS (ESCRITURA CON VALIDACIÓN EN PIPELINE BEHAVIOR)
 2) 📖 DEMO 2: EJECUCIÓN DE QUERIES (LECTURA HIPER-RÁPIDA DIRECTA DEL READ MODEL)
 3) 🔄 DEMO 3: FLUJO COMPLETO CQRS (CREACIÓN -> EMISIÓN -> CONSULTA EN VIVO)
```

---

### ✍️ DEMO 1: EJECUCIÓN DE COMMANDS (PILA DE ESCRITURA MEDIATR)

Ingresa `1` y presiona Enter.

**Salida en consola**:
```text
1. Probando Command con Payload Inválido (Monto = 0):
   Status HTTP: 422 (ValidationBehavior -> 422 Unprocessable Entity)
   Body: {"detail": "VALIDATION_FAILED: El monto debe ser mayor a cero."}

2. Probando Command Válido ('CreatePolicyCommand'):
   Status HTTP: 201 Created
   Respuesta:
   {
     "status": "CREATED",
     "policy_id": "POL-NET9-8F12AB90",
     "message": "Comando ejecutado exitosamente mediante MediatR Pipeline Behavior.",
     "trace_id": "9012ab78"
   }
```

* **Qué decir a la cámara**:
  > *"Observen cómo los comandos pasan por el Pipeline Behavior de MediatR; si los datos son inválidos, el ValidationBehavior detiene la ejecución respondiendo un 422 de forma transparente."*

---

### 📖 DEMO 2: EJECUCIÓN DE QUERIES (PILA DE LECTURA READ MODEL)

Ingresa `2` y presiona Enter.

**Salida en consola**:
```text
Consultando Query 'GetPolicyByIdQuery' para ID 'POL-NET9-8F12AB90':
 HTTP Status: 200 OK
 Proyección Read Model (Respuesta < 2ms):
{
  "status": "SUCCESS",
  "source": "READ_MODEL_PROJECTION",
  "data": {
    "id": "POL-NET9-8F12AB90",
    "display_title": "Póliza de HOGAR - Cliente Ejemplo",
    "status": "DRAFT",
    "amount_formatted": "$1,200.00 USD"
  }
}
```

* **Qué decir a la cámara**:
  > *"A diferencia de las escrituras, las consultas no tocan la entidad de dominio ni abren transacciones ACID; leen directamente las proyecciones DTO optimizadas en menos de 2 milisegundos."*

---

### 🔄 DEMO 3: FLUJO COMPLETO CQRS (.NET 9 MEDIATR)

Ingresa `3` y presiona Enter.

**Salida en consola**:
```text
[PASO 1] Ejecutando 'CreatePolicyCommand':
 Póliza creada con ID: POL-NET9-771A (Estado inicial: DRAFT)

[PASO 2] Consultando estado previo en el Read Model ('GetPolicyByIdQuery'):
 Estado en Read Model: DRAFT

[PASO 3] Ejecutando comando de emisión 'EmitPolicyCommand':
 Resultado Emisión: EMITTED -> Póliza POL-NET9-771A ahora en ACTIVE

[PASO 4] Consultando estado final actualizado en Read Model:
 Estado Final en Read Model: ACTIVE | Referencia Pago: PAY-REF-998811
```

---

## 🎯 RESUMEN DE COMANDOS RÁPIDOS

```bash
# 1. Ubicarse en la carpeta
cd /Users/deals/Documents/GIT/TestArquitectura/pregunta_07

# 2. Desplegar servicios en Podman
podman compose up -d --build

# 3. Lanzar la demostración interactiva
./load_test/run_visual_demo.sh
```
