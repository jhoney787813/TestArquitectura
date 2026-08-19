# Guión de Sustentación para Cámara - Ejercicio 5: Observabilidad y Pipeline Behavior

**Formato**: Guión para video de presentación / Entrevista técnica en vivo  
**Rol**: Arquitecto Senior de Software  
**Enfoque**: Metodología **Why-Driven Design (WDD)**, **Pipeline Behaviors (MediatR CQRS)**, Modelo de Madurez de Richardson, OpenTelemetry y Atributos ISO 25010  
**Duración Estimada**: 4 a 5 minutos  

---

## 🎬 ESCENA 1: MARCO METODOLÓGICO Y PIPELINE BEHAVIOR (0:00 - 1:15)

**[Mirada directa a la cámara, postura firme, analítica y profesional]**

> **"Hola a todos.**
> 
> Abordamos el **Ejercicio 5: Observabilidad, Gestión de Excepciones y Diagnóstico del Código `catch(Exception ex) { return BadRequest(); }`**.
> 
> En mi experiencia como Arquitecto de Software en arquitecturas empresariales Clean Architecture con patrones CQRS, **el manejo de errores NUNCA debe hacerse dentro de los controladores ni en los Handlers mediante bloques try-catch repetitivos**.
> 
> En su lugar, implementamos la solución de **Pipeline Behaviors (Cross-Cutting Concerns en MediatR)**:
> 
> - **`ValidationBehavior`**: Intercepta los comandos antes de llegar al handler. Si las reglas de negocio o FluentValidation fallan, detiene la ejecución inmediatamente y retorna una respuesta semántica alineada al **Nivel 2 de Richardson (`HTTP 422 Unprocessable Entity`)**.
> - **`UnhandledExceptionBehavior`**: Envuelve la canalización, captura excepciones no manejadas, les inyecta el `TraceId` de **OpenTelemetry**, las registra en formato JSON estructurado con **Serilog/Loki** y las convierte en respuestas **RFC 7807 (ProblemDetails)**.
> - **`PerformanceBehavior`**: Mide latencias y alimenta el histograma de **Prometheus**."

---

## 🔍 ESCENA 2: DIAGNÓSTICO DEL PROBLEMA (PREGUNTA A) (1:15 - 2:30)

**[Tono estructurado evaluando los 4 fallos del código entregado]**

> **"Respondiendo a la Pregunta A: ¿Qué problemas vemos en `catch(Exception ex) { return BadRequest(); }`?**
> 
> 1. **Anti-patrón de Captura Ciega en Controladores**: Escribir try-catch en cada controlador duplica código y viola el principio DRY.
> 2. **Pérdida de Trazabilidad Distribuida**: Al capturar `catch(Exception ex)` y hacer un `return BadRequest()` ciego, se corta la propagación de la cabecera W3C `traceparent` (`TraceId` / `SpanId`), impidiendo correlacionar el fallo en Jaeger o Grafana.
> 3. **Violación del Modelo de Madurez de Richardson (Nivel 2/3)**: Responder siempre `400 BadRequest` destruye la semántica REST. Un recurso inexistente debe ser `404 Not Found`, una regla de negocio violada debe ser `422 Unprocessable Entity` y un fallo de base de datos debe ser `503 Service Unavailable`.
> 4. **Mezcla de Excepciones de Dominio e Infraestructura**: Trata por igual una precondición de negocio que un puntero nulo o timeout de red."

---

## 📊 ESCENA 3: DISEÑO DE LA ARQUITECTURA DE OBSERVABILIDAD (PREGUNTA B) (2:30 - 3:45)

**[Mostrar el diagrama C4 o explicar los 3 pilares de telemetría]**

> **"Respondiendo a la Pregunta B: Diseñamos una arquitectura basada en los 3 Pilares de Observabilidad integrados en Pipeline Behaviors:**
> 
> 1. **Trazas Distribuidas**: **OpenTelemetry SDK** inyectando el encabezado W3C `traceparent` para rastrear peticiones end-to-end en **Jaeger**.
> 2. **Métricas RED/USE**: Exponemos el endpoint `/metrics` en formato **Prometheus** para medir tasa de peticiones, histogramas de latencia y contador de errores por código HTTP.
> 3. **Logs Estructurados en JSON**: Utilizamos **Serilog** exportando registros hacia **Grafana Loki** enriquecidos con `TraceId`, `SpanId` y `Environment`.
> 4. **Formato Standard RFC 7807 (ProblemDetails)**: Respuestas HTTP de error estandarizadas respetando el Modelo de Madurez de Richardson."

---

## 🎯 ESCENA 4: CONCLUSIÓN Y DEMOSTRACIÓN (3:45 - 4:30)

> **"En conclusión: reemplazar el anti-patrón `catch(Exception ex) { return BadRequest(); }` por un Pipeline Behavior centralizado con OpenTelemetry y el Modelo de Richardson reduce el tiempo de diagnóstico de horas a minutos.**
> 
> Todo el código funcional, la prueba interactiva en Podman en el puerto 8005, los diagramas C4 Model para Draw.io y la guía de Kubernetes están listos en la carpeta `pregunta_05/`. ¡Muchas gracias!"**
