# Test de Arquitectura de Software - Proceso de Selección Senior

**Postulante**: Jhon E. / Arquitecto Senior de Software  
**Cuenta de GitHub**: [`jhoney787813`](https://github.com/jhoney787813)  
**Repositorio Oficial**: [`https://github.com/jhoney787813/TestArquitectura`](https://github.com/jhoney787813/TestArquitectura)  
**Metodología de Arquitectura**: **Why-Driven Design (WDD)** | **Modelo C4** | **Clean Architecture (.NET 9)** | **Pipeline Behaviors (MediatR CQRS)** | **ISO/IEC 25010 Quality Attributes** | **Apache Kafka & Observability**  

---

## 📌 Mensaje Dirigido al Comité Evaluador de Arquitectura

Estimado equipo evaluador y líderes técnicos del proceso de selección:

Este repositorio contiene la solución práctica, documentada y desplegable del **Examen Técnico de Arquitectura de Software (`Prueba Técnica - FWK Architect.docx`)**. 

Cada uno de los **5 Ejercicios Propuestos** ha sido **construido como un proyecto funcional ejecutable en contenedores OCI (Podman / Docker)**, respaldado por **evidencia empírica en tiempo real**, **playbooks operacionales en Kubernetes**, **diagramas NATIVOS para Draw.io (.drawio XML y .mmd Mermaid)**, **diagramas C4 Model** y una **sustentación guiada por la metodología Why-Driven Design (WDD)**.

El objetivo de esta entrega es demostrar no solo el conocimiento de patrones avanzados de microservicios, resiliencia, observabilidad y seguridad distribuida, sino la **experiencia práctica y *expertise* en el sector de arquitectura empresarial**, traduciendo decisiones técnicas complejas en valor de negocio medible, alta tolerancia a fallos y excelente comunicación técnica.

---

## 🗺️ Índice Directo de Respuestas por Ejercicio y Pregunta

Para facilitar la revisión por parte del comité evaluador, a continuación se detallan los enlaces directos a la respuesta, código fuente, diagramas de arquitectura y guiones de sustentación de cada ejercicio:

---

### 🔴 Ejercicio 1: Diagnóstico de Performance (CPU 10%, RAM 30%, P95 = 8s)

- **Pregunta Abordada**: *¿Qué investigaría si una API REST consume CPU 10%, RAM 30% y P95 es de 8 segundos?*
- 📄 **Respuesta & Justificación Técnica**: [`pregunta_01/JUSTIFICACION_TECNICA.md`](pregunta_01/JUSTIFICACION_TECNICA.md)  
  *(Explicación con la **Analogía de las Ventanillas del Banco**: I/O Wait, Thread Pool Starvation y Connection Pool Exhaustion)*
- 🎬 **Guión de Sustentación para Cámara**: [`pregunta_01/GUION_SUSTENTACION.md`](pregunta_01/GUION_SUSTENTACION.md)
- 📹 **Guía Paso a Paso para Grabación de Video**: [`pregunta_01/GUIA_PRUEBA_VIDEO.md`](pregunta_01/GUIA_PRUEBA_VIDEO.md)
- 📊 **Playbook de Diagnóstico en Kubernetes**: [`pregunta_01/kubernetes/KUBERNETES_DIAGNOSTICO.md`](pregunta_01/kubernetes/KUBERNETES_DIAGNOSTICO.md) y [`pregunta_01/kubernetes/diagnostic_commands.sh`](pregunta_01/kubernetes/diagnostic_commands.sh)
- 🖥️ **Script de Demostración Visual (ANTES vs DESPUÉS)**: [`pregunta_01/load_test/run_visual_demo.sh`](pregunta_01/load_test/run_visual_demo.sh)  
  *(Demuestra la caída de latencia de 8.17s a **15 milisegundos**, una mejora de **> 1,000x**)*
- 💻 **Código Fuente y Despliegue en Podman**:
  - API REST Simulada: [`pregunta_01/app/main.py`](pregunta_01/app/main.py)
  - Servicio Downstream Lento: [`pregunta_01/mock_downstream/server.py`](pregunta_01/mock_downstream/server.py)
  - Orquestador Compose: [`pregunta_01/docker-compose.yml`](pregunta_01/docker-compose.yml)

---

### 🛡️ Ejercicio 2: Patrones, Escalabilidad y Resiliencia (Emisión de Pólizas)

- **Preguntas Abordadas**:
  - **A)** *Realice el diseño más conveniente para la emisión de una póliza (DB, Email, SMS, Audit)*
  - **B)** *¿Qué pasa si SavePolicy falla?*
  - **C)** *¿Qué pasa si SendEmail falla?*
  - **D)** *¿Qué pasa si SMS está caído?*
  - **E)** *¿Qué pasa si Audit falla? ¿Dónde persistiría AuditService?*
- 📄 **Respuestas Detalladas A-E & Sustentación WDD**: [`pregunta_02/JUSTIFICACION_TECNICA.md`](pregunta_02/JUSTIFICACION_TECNICA.md)  
  *(Metodología **Why-Driven Design (WDD)**, **Analogía del Tiquete de Avión**, Atributos ISO/IEC 25010 y Matriz de Trade-offs)*
- 🎨 **Diagrama de Arquitectura de Componentes para Draw.io**:
  - Archivo XML Nativo para Draw.io: [`pregunta_02/diagrams/component_architecture.drawio`](pregunta_02/diagrams/component_architecture.drawio)
  - Código Mermaid Importable: [`pregunta_02/diagrams/component_architecture.mmd`](pregunta_02/diagrams/component_architecture.mmd)
- 🎬 **Guión de Sustentación para Cámara**: [`pregunta_02/GUION_SUSTENTACION.md`](pregunta_02/GUION_SUSTENTACION.md)
- 📹 **Guía Paso a Paso para Grabación de Video**: [`pregunta_02/GUIA_PRUEBA_VIDEO.md`](pregunta_02/GUIA_PRUEBA_VIDEO.md)
- 📊 **Playbook de Diagnóstico en Kubernetes**: [`pregunta_02/kubernetes/KUBERNETES_DIAGNOSTICO.md`](pregunta_02/kubernetes/KUBERNETES_DIAGNOSTICO.md) y [`pregunta_02/kubernetes/diagnostic_commands.sh`](pregunta_02/kubernetes/diagnostic_commands.sh)
- 🖥️ **Script CLI Interactivo de Demostración (Escenarios A, B, C, D y E)**: [`pregunta_02/load_test/run_visual_demo.sh`](pregunta_02/load_test/run_visual_demo.sh)
- 💻 **Código Fuente y Despliegue en Podman**:
  - API Transactional Outbox: [`pregunta_02/app/main.py`](pregunta_02/app/main.py)
  - Worker Asíncrono (Retries + DLQ): [`pregunta_02/workers/notification_worker.py`](pregunta_02/workers/notification_worker.py)
  - Gateways con Circuit Breaker & OpenSearch: [`pregunta_02/mock_services/external_gateways.py`](pregunta_02/mock_services/external_gateways.py)
  - Orquestador Compose: [`pregunta_02/docker-compose.yml`](pregunta_02/docker-compose.yml)

---

### ⚡ Ejercicio 3: Real Time Architecture (Emisión, Inspección, Siniestros)

- **Pregunta Abordada**: *¿Cómo implementaría la solución técnica en tiempo real para mostrar el estado de Emisión, Inspección y Siniestros? Debe discutir WebSockets, SignalR, SSE, Polling y explicar Trade-offs.*
- 📄 **Respuesta & Sustentación WDD**: [`pregunta_03/JUSTIFICACION_TECNICA.md`](pregunta_03/JUSTIFICACION_TECNICA.md)  
  *(Metodología **Why-Driven Design (WDD)**, **Analogía de Uber / Domino's Pizza Tracker**, **Apache Kafka Event Backbone**, **SignalR Hubs / SSE Gateway** y **Redis Pub/Sub Backplane**)*
- 📐 **Diagrama C4 Model Nivel 2 (Container Diagram) para Draw.io**:
  - Archivo XML Nativo C4 Model para Draw.io: [`pregunta_03/diagrams/c4_model_realtime_architecture.drawio`](pregunta_03/diagrams/c4_model_realtime_architecture.drawio)
  - Código C4 Model Mermaid Importable: [`pregunta_03/diagrams/c4_model_realtime_architecture.mmd`](pregunta_03/diagrams/c4_model_realtime_architecture.mmd)
- 🎬 **Guión de Sustentación para Cámara**: [`pregunta_03/GUION_SUSTENTACION.md`](pregunta_03/GUION_SUSTENTACION.md)
- 📹 **Guía Paso a Paso para Grabación de Video**: [`pregunta_03/GUIA_PRUEBA_VIDEO.md`](pregunta_03/GUIA_PRUEBA_VIDEO.md)
- 📊 **Playbook de Diagnóstico en Kubernetes**: [`pregunta_03/kubernetes/KUBERNETES_DIAGNOSTICO.md`](pregunta_03/kubernetes/KUBERNETES_DIAGNOSTICO.md) y [`pregunta_03/kubernetes/diagnostic_commands.sh`](pregunta_03/kubernetes/diagnostic_commands.sh)
- 🖥️ **Script de Demostración SSE / WebSockets en Tiempo Real**: [`pregunta_03/load_test/run_visual_demo.sh`](pregunta_03/load_test/run_visual_demo.sh)  
  *(Transmisión continua de eventos de Emisión, Inspección y Siniestros sin refrescar la pantalla)*
- 💻 **Código Fuente y Despliegue en Podman**:
  - Real-Time Gateway API (SSE, WebSockets, SignalR): [`pregunta_03/app/main.py`](pregunta_03/app/main.py)
  - Generador de Eventos Distribuidos Kafka: [`pregunta_03/mock_events/event_generator.py`](pregunta_03/mock_events/event_generator.py)
  - Orquestador Compose: [`pregunta_03/docker-compose.yml`](pregunta_03/docker-compose.yml)

---

### 🔐 Ejercicio 4: Authentication & Authorization (REST, SOAP, WebSockets & Revocación)

- **Preguntas Abordadas**:
  - **A)** *Diseñe el esquema de seguridad unificado para REST, SOAP y WebSockets.*
  - **B)** *¿Cómo revoca tokens? (Redis Token Blacklisting con TTL + Short-Lived Access Tokens + Refresh Token Rotation)*
- 📄 **Respuestas Detalladas A y B & Sustentación WDD**: [`pregunta_04/JUSTIFICACION_TECNICA.md`](pregunta_04/JUSTIFICACION_TECNICA.md)  
  *(Metodología **Why-Driven Design (WDD)**, **Clean Architecture (.NET 9)**, **Analogía del Pasaporte Biométrico e Interpol**, Atributos ISO/IEC 25010 y Puntos Clave de Exposición)*
- 📐 **Diagrama C4 Model Nivel 2 (Container Diagram) para Draw.io**:
  - Archivo XML Nativo C4 Model para Draw.io: [`pregunta_04/diagrams/c4_security_architecture.drawio`](pregunta_04/diagrams/c4_security_architecture.drawio)
  - Código C4 Model Mermaid Importable: [`pregunta_04/diagrams/c4_security_architecture.mmd`](pregunta_04/diagrams/c4_security_architecture.mmd)
- 🎬 **Guión de Sustentación para Cámara**: [`pregunta_04/GUION_SUSTENTACION.md`](pregunta_04/GUION_SUSTENTACION.md)
- 📹 **Guía Paso a Paso para Grabación de Video**: [`pregunta_04/GUIA_PRUEBA_VIDEO.md`](pregunta_04/GUIA_PRUEBA_VIDEO.md)
- 📊 **Playbook de Diagnóstico en Kubernetes**: [`pregunta_04/kubernetes/KUBERNETES_DIAGNOSTICO.md`](pregunta_04/kubernetes/KUBERNETES_DIAGNOSTICO.md) y [`pregunta_04/kubernetes/diagnostic_commands.sh`](pregunta_04/kubernetes/diagnostic_commands.sh)
- 🌐 **Aplicación Cliente Web Multi-Protocolo por Pestañas (REST, SOAP & WS)**:
  - URL del Cliente Contenedorizado: [`http://localhost:8084`](http://localhost:8084)
  - Código Fuente HTML/JS: [`pregunta_04/client/websocket_client.html`](pregunta_04/client/websocket_client.html)
- 🖥️ **Script CLI de Demostración Visual en Consola**: [`pregunta_04/load_test/run_visual_demo.sh`](pregunta_04/load_test/run_visual_demo.sh)
- 💻 **Código Fuente y Despliegue en Podman**:
  - API Gateway Clean Architecture (.NET 9 / FastAPI): [`pregunta_04/app/main.py`](pregunta_04/app/main.py)
  - Dockerfile del Cliente WebSocket: [`pregunta_04/client/Dockerfile`](pregunta_04/client/Dockerfile)
  - Orquestador Compose: [`pregunta_04/docker-compose.yml`](pregunta_04/docker-compose.yml)

---

### 📊 Ejercicio 5: Observability (Diagnóstico catch(Exception ex), Pipeline Behaviors & Richardson)

- **Preguntas Abordadas**:
  - **A)** *¿Qué problemas ve en catch(Exception ex) { return BadRequest(); }?*
  - **B)** *Diseñe observabilidad para la solución técnica (Herramientas, librerías, OpenTelemetry, Prometheus, Grafana, Jaeger, Loki, ProblemDetails RFC 7807 y Modelo de Richardson)*
- 📄 **Respuestas Detalladas A y B & Sustentación WDD**: [`pregunta_05/JUSTIFICACION_TECNICA.md`](pregunta_05/JUSTIFICACION_TECNICA.md)  
  *(Metodología **Why-Driven Design (WDD)**, **Patrón Pipeline Behavior (MediatR / CQRS)**, **Analogía de la Caja Negra de Aviación**, **Modelo de Madurez de Richardson (Nivel 2/3)** y Atributos ISO/IEC 25010)*
- 📐 **Diagrama C4 Model Nivel 2 (Container Diagram) para Draw.io**:
  - Archivo XML Nativo C4 Model para Draw.io: [`pregunta_05/diagrams/c4_observability_architecture.drawio`](pregunta_05/diagrams/c4_observability_architecture.drawio)
  - Código C4 Model Mermaid Importable: [`pregunta_05/diagrams/c4_observability_architecture.mmd`](pregunta_05/diagrams/c4_observability_architecture.mmd)
- 🎬 **Guión de Sustentación para Cámara**: [`pregunta_05/GUION_SUSTENTACION.md`](pregunta_05/GUION_SUSTENTACION.md)
- 📹 **Guía Paso a Paso para Grabación de Video**: [`pregunta_05/GUIA_PRUEBA_VIDEO.md`](pregunta_05/GUIA_PRUEBA_VIDEO.md)
- 📊 **Playbook de Diagnóstico en Kubernetes**: [`pregunta_05/kubernetes/KUBERNETES_DIAGNOSTICO.md`](pregunta_05/kubernetes/KUBERNETES_DIAGNOSTICO.md) y [`pregunta_05/kubernetes/diagnostic_commands.sh`](pregunta_05/kubernetes/diagnostic_commands.sh)
- 🖥️ **Script CLI de Demostración Visual (Demostración del Anti-patrón vs Solución Técnica)**: [`pregunta_05/load_test/run_visual_demo.sh`](pregunta_05/load_test/run_visual_demo.sh)
- 💻 **Código Fuente y Despliegue en Podman**:
  - API de Observabilidad (.NET 9 / FastAPI): [`pregunta_05/app/main.py`](pregunta_05/app/main.py)
  - Orquestador Compose: [`pregunta_05/docker-compose.yml`](pregunta_05/docker-compose.yml)

---

## 🚀 Guía Rápida de Ejecución Práctica en Podman / Docker

Todos los 5 ejercicios pueden ejecutarse de manera independiente y en simultáneo sin conflictos de puertos:

### Para probar el Ejercicio 1 (Diagnóstico de Performance - Puerto 8000):
```bash
cd pregunta_01
podman compose up -d --build
./load_test/run_visual_demo.sh
```

### Para probar el Ejercicio 2 (Resiliencia y Outbox Pattern - Puerto 8001):
```bash
cd pregunta_02
podman compose up -d --build
./load_test/run_visual_demo.sh
```

### Para probar el Ejercicio 3 (Real Time Architecture - Puerto 8002):
```bash
cd pregunta_03
podman compose up -d --build
./load_test/run_visual_demo.sh
```

### Para probar el Ejercicio 4 (Seguridad Multi-Protocolo - Puertos 8003 y 8084):
```bash
cd pregunta_04
podman compose up -d --build
./load_test/run_visual_demo.sh
# O abre en tu navegador el cliente interactivo: http://localhost:8084
```

### Para probar el Ejercicio 5 (Observabilidad y Pipeline Behavior - Puerto 8005):
```bash
cd pregunta_05
podman compose up -d --build
./load_test/run_visual_demo.sh
```

---

## 🎨 Cómo visualizar los Diagramas en Draw.io (diagrams.net)

1. Abre **[app.diagrams.net](https://app.diagrams.net)** en tu navegador web.
2. Selecciona **"Abrir diagrama existente"** y selecciona cualquiera de los archivos del repositorio:
   - Diagrama de Componentes Ejercicio 2: `pregunta_02/diagrams/component_architecture.drawio`
   - Diagrama C4 Model Ejercicio 3: `pregunta_03/diagrams/c4_model_realtime_architecture.drawio`
   - Diagrama C4 Model Ejercicio 4: `pregunta_04/diagrams/c4_security_architecture.drawio`
   - Diagrama C4 Model Ejercicio 5: `pregunta_05/diagrams/c4_observability_architecture.drawio`
3. *Método Alternativo*: En Draw.io ve a **Organizar -> Insertar -> Avanzado -> Mermaid** y pega el contenido del archivo `.mmd` correspondiente.

---

## 🎯 Atributos de Calidad ISO/IEC 25010 y Compromisos (Trade-offs)

Bajo la norma **ISO/IEC 25010**, los proyectos destacan los siguientes compromisos asumidos:

- **Consistencia Eventual vs. Consistencia Fuerte Inmediata**: Aceptamos consistencia eventual de segundos en canales de notificación (Email/SMS) a cambio de garantizar la respuesta HTTP en **0.23 ms** y un SLA de disponibilidad del 99.99%.
- **Tolerancia a Fallos vs. Complejidad Operativa**: Incurrimos en administrar workers asíncronos y colas DLQ a cambio de aislar completamente el core del negocio de caídas en proveedores de terceros.
- **Server-Sent Events vs WebSockets**: SSE es seleccionado para dashboards de monitoreo en tiempo real por su ligereza HTTP/2 nativa, reconexión automática y facilidad para atravesar proxies corporativos.
- **Validación estatutaria (RS256) vs Consulta a BD en Seguridad**: Usamos tokens JWT RS256 de validación local y una **Redis Token Blacklist con TTL** para verificar revocaciones en **< 1ms**, evitando sobrecargar la BD relacional en cada petición HTTP/SOAP/WS.
- **Centralización via Pipeline Behavior vs Try-Catch en Controladores**: Usamos Pipeline Behaviors en MediatR CQRS para interceptar excepciones sin duplicar código en controladores, aceptando una ligera sobrecarga CPU (< 1%) por instrumentación OpenTelemetry a cambio de un MTTR de minutos.

---
*Repositorio creado, mantenido y sustentado por Jhon E. para el proceso de selección de Arquitecto de Software.*
