# Guía Paso a Paso para la Grabación del Video de Sustentación (Ejercicio 5)

Esta guía explica exactamente qué comandos ejecutar y qué mostrar en pantalla para demostrar la observabilidad, el patrón de **Pipeline Behavior (MediatR CQRS)**, el mapeo semántico del **Modelo de Richardson** y la exportación de métricas de Prometheus.

---

## 🎬 PREPARACIÓN PREVIA DE LA TERMINAL

```bash
cd /Users/deals/Documents/GIT/TestArquitectura/pregunta_05
```

---

## 📹 GUÍA DE DEMOSTRACIÓN PASO A PASO EN LA CONSOLA

### 🔹 Paso 1: Ejecutar el Menú Interactivo de Observabilidad
```bash
./load_test/run_visual_demo.sh
```

En la pantalla aparecerá:

```text
==========================================================================
    📊 DEMOSTRACIÓN DE OBSERVABILIDAD, MODELO DE RICHARDSON Y OPENTELEMETRY
==========================================================================

Selecciona el escenario a probar en la consola:
 1) 🔴 DEMO 1: DIAGNÓSTICO DEL ANTIPATRÓN catch(Exception ex) { return BadRequest(); }
 2) 🟢 DEMO 2: SOLUCIÓN TÉCNICA CON MAPEO DE RICHARDSON & RFC 7807 (HTTP 404, 409, 422, 503)
 3) 🔍 DEMO 3: TRAZABILIDAD DISTRIBUIDA OPENTELEMETRY (Header W3C traceparent & TraceId)
 4) 📈 DEMO 4: EXPORTADOR DE MÉTRICAS PROMETHEUS (/metrics)
```

---

### 🔴 DEMO 1: DIAGNÓSTICO DEL ANTIPATRÓN catch(Exception ex) { return BadRequest(); }

Ingresa `1` y presiona Enter.

**Salida en consola**:
```text
1. Petición por recurso inexistente ('not-found'):
   Status HTTP: 400 (¡Debería ser 404 Not Found!)
   Body: {"message": "BadRequest genérico: Ocurrió un error sin traza..."}

2. Petición con falla de Base de Datos ('db-error'):
   Status HTTP: 400 (¡Debería ser 503 Service Unavailable!)

--> CONCLUSIÓN PREGUNTA A: catch(Exception ex) enmascara la causa real, destruye la semántica REST y borra la traza.
```

* **Qué decir a la cámara**:
  > *"En mi experiencia como Arquitecto de Software, escribir try-catch en cada controlador y hacer return BadRequest() ciego duplica código, destruye las trazas y oculta la causa raíz."*

---

### 🟢 DEMO 2: SOLUCIÓN TÉCNICA CON PIPELINE BEHAVIOR & MODELO DE RICHARDSON

Ingresa `2` y presiona Enter.

**Salida en consola**:
```text
Probando escenario 'Recurso no encontrado' (not-found):
 HTTP Status: 404 | Content-Type: application/problem+json
 Header TraceId: 97420f28323640838051c9d71d28c17c
 ProblemDetails RFC 7807 JSON:
{
  "type": "https://api.seguros.com/errors/resource_not_found",
  "title": "Resource Not Found",
  "status": 404,
  "detail": "El recurso 'Póliza' con ID 'not-found' no existe.",
  "code": "RESOURCE_NOT_FOUND",
  "instance": "/api/v1/good-practice/policies/not-found",
  "trace_id": "97420f28323640838051c9d71d28c17c"
}
--------------------------------------------------
Probando escenario 'Violación de Regla de Negocio' (rule-error):
 HTTP Status: 422 Unprocessable Entity
--------------------------------------------------
Probando escenario 'Falla Técnica Downstream' (db-error):
 HTTP Status: 503 Service Unavailable
```

* **Qué decir a la cámara**:
  > *"Mediante Pipeline Behaviors (ValidationBehavior y UnhandledExceptionBehavior), interceptamos las excepciones en la canalización sin tocar los controladores, traduciendo cada tipo de error a su código semántico de Richardson en formato RFC 7807."*

---

### 🔍 DEMO 3: TRAZABILIDAD DISTRIBUIDA W3C `traceparent`

Ingresa `3` y presiona Enter.

**Salida en consola**:
```text
Enviando cabecera W3C traceparent entrante: 00-4bf92f3577b34da6a3ce929d0e0e4736-00f067aa0ba902b7-01
TraceParent devuelto en respuesta: 00-4bf92f3577b34da6a3ce929d0e0e4736-00f067aa0ba902b7-01
Trace-ID extraído: 4bf92f3577b34da6a3ce929d0e0e4736
```

---

### 📈 DEMO 4: EXPORTADOR DE MÉTRICAS PROMETHEUS (GET /metrics)

Ingresa `4` y presiona Enter.

**Salida en consola**:
```text
# HELP http_requests_total Total number of HTTP requests processed.
# TYPE http_requests_total counter
http_requests_total 12

requests_by_status{code="200"} 5
requests_by_status{code="404"} 2
requests_by_status{code="422"} 2
requests_by_status{code="503"} 3
```

---

## 🎯 RESUMEN DE COMANDOS RÁPIDOS

```bash
# 1. Ubicarse en la carpeta
cd /Users/deals/Documents/GIT/TestArquitectura/pregunta_05

# 2. Desplegar servicios en Podman
podman compose up -d --build

# 3. Lanzar la demostración interactiva
./load_test/run_visual_demo.sh
```
