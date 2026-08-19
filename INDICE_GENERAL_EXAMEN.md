# Índice General y Documentación Completa del Examen de Arquitectura

**Postulante**: Jhon E. / Arquitecto Senior de Software  
**Cuenta de GitHub**: [`jhoney787813`](https://github.com/jhoney787813)  
**Repositorio Oficial**: [`https://github.com/jhoney787813/TestArquitectura`](https://github.com/jhoney787813/TestArquitectura)  
**Metodología de Arquitectura**: **Why-Driven Design (WDD)** | **Modelo C4** | **Clean Architecture (.NET 9)** | **CQRS & Patrón Mediator** | **Pipeline Behaviors** | **ISO/IEC 25010**  

---

## 📌 Guía de Navegación del Examen Técnico

Este documento sirve como el **índice detallado de navegación** para explorar la solución de cada uno de los **7 Ejercicios Propuestos** en la prueba de arquitectura de software.

Cada carpeta contiene la solución en código funcional OCI, sustentación técnica bajo WDD, diagramas C4 nativos para Draw.io (`.drawio` y `.mmd`), guiones para presentación ante cámara, guías de grabación de video y playbooks operacionales de Kubernetes.

---

## 🗺️ Desglose Detallado por Ejercicio

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
- 🖥️ **Script CLI de Demostración Visual**: [`pregunta_05/load_test/run_visual_demo.sh`](pregunta_05/load_test/run_visual_demo.sh)
- 💻 **Código Fuente y Despliegue en Podman**:
  - API de Observabilidad (.NET 9 / FastAPI): [`pregunta_05/app/main.py`](pregunta_05/app/main.py)
  - Orquestador Compose: [`pregunta_05/docker-compose.yml`](pregunta_05/docker-compose.yml)

---

### 🚀 Ejercicio 6: Performance Engineering (Escalado 5x: 100 TPS ──► 500 TPS)

- **Preguntas Abordadas**:
  - **A)** *¿Qué mediría primero? (Métricas RED/USE, Latencias P95/P99, Connection Pool Starvation, I/O Wait, GC Pauses)*
  - **B)** *¿Cómo escalaría? (Fase 1: Async I/O & Índices SQL, Fase 2: Redis Caching > 85% Hit Ratio & Outbox Asíncrono, Fase 3: CQRS Read Replicas BD, DB Proxy & K8s HPA)*
- 📄 **Respuestas Detalladas A y B & Resumen Ejecutivo del Arquitecto**: [`pregunta_06/JUSTIFICACION_TECNICA.md`](pregunta_06/JUSTIFICACION_TECNICA.md)  
  *(Metodología **Why-Driven Design (WDD)**, **Analogía del Peaje de Autopista**, Hoja de Ruta de Escalado y Resumen Ejecutivo)*

---

### 🔀 Ejercicio 7: Patrón CQRS y Mediator en .NET 9 (Command Query Responsibility Segregation)

- **Pregunta Abordada**: *Ejecute la arquitectura implementando CQRS y el patrón Mediator para la pregunta 7, realice el análisis y justifique la implementación.*
- 📄 **Respuestas & Sustentación WDD**: [`pregunta_07/JUSTIFICACION_TECNICA.md`](pregunta_07/JUSTIFICACION_TECNICA.md)  
  *(Metodología **Why-Driven Design (WDD)**, **Analogía de la Cocina del Restaurante (Chef vs Mesero)**, **Clean Architecture (.NET 9)**, **MediatR Pipeline Behaviors**, **Read/Write Models Separados** y **Consistencia Eventual**)*
- 📐 **Diagrama C4 Model Nivel 2 (Container Diagram) para Draw.io**:
  - Archivo XML Nativo C4 Model para Draw.io: [`pregunta_07/diagrams/cqrs_mediator_architecture.drawio`](pregunta_07/diagrams/cqrs_mediator_architecture.drawio)
  - Código C4 Model Mermaid Importable: [`pregunta_07/diagrams/cqrs_mediator_architecture.mmd`](pregunta_07/diagrams/cqrs_mediator_architecture.mmd)
- 🎬 **Guión de Sustentación para Cámara**: [`pregunta_07/GUION_SUSTENTACION.md`](pregunta_07/GUION_SUSTENTACION.md)
- 📹 **Guía Paso a Paso para Grabación de Video**: [`pregunta_07/GUIA_PRUEBA_VIDEO.md`](pregunta_07/GUIA_PRUEBA_VIDEO.md)
- 📊 **Playbook de Diagnóstico en Kubernetes**: [`pregunta_07/kubernetes/KUBERNETES_DIAGNOSTICO.md`](pregunta_07/kubernetes/KUBERNETES_DIAGNOSTICO.md) y [`pregunta_07/kubernetes/diagnostic_commands.sh`](pregunta_07/kubernetes/diagnostic_commands.sh)
- 🖥️ **Script CLI de Demostración Visual (Comandos vs Consultas en Vivo)**: [`pregunta_07/load_test/run_visual_demo.sh`](pregunta_07/load_test/run_visual_demo.sh)
- 💻 **Código Fuente Nativo C# .NET 9**:
  - Proyecto C# .NET 9: [`pregunta_07/app/CqrsMediatorApi.csproj`](pregunta_07/app/CqrsMediatorApi.csproj)
  - Program.cs (.NET 9 Web API): [`pregunta_07/app/Program.cs`](pregunta_07/app/Program.cs)
  - Dominio: [`pregunta_07/app/Domain/Entities/Policy.cs`](pregunta_07/app/Domain/Entities/Policy.cs)
  - Commands & Handlers: [`pregunta_07/app/Application/Commands/CreatePolicyCommandHandler.cs`](pregunta_07/app/Application/Commands/CreatePolicyCommandHandler.cs)
  - Queries & Handlers: [`pregunta_07/app/Application/Queries/GetPolicyByIdQueryHandler.cs`](pregunta_07/app/Application/Queries/GetPolicyByIdQueryHandler.cs)
  - Pipeline Behaviors: [`pregunta_07/app/Application/Behaviors/ValidationBehavior.cs`](pregunta_07/app/Application/Behaviors/ValidationBehavior.cs)
  - Controller ASP.NET Core 9: [`pregunta_07/app/Controllers/PoliciesController.cs`](pregunta_07/app/Controllers/PoliciesController.cs)
  - Orquestador Compose: [`pregunta_07/docker-compose.yml`](pregunta_07/docker-compose.yml)

---

## 🎨 Cómo visualizar los Diagramas en Draw.io (diagrams.net)

1. Abre **[app.diagrams.net](https://app.diagrams.net)** en tu navegador web.
2. Selecciona **"Abrir diagrama existente"** y selecciona cualquiera de los archivos del repositorio:
   - Ejercicio 2: `pregunta_02/diagrams/component_architecture.drawio`
   - Ejercicio 3: `pregunta_03/diagrams/c4_model_realtime_architecture.drawio`
   - Ejercicio 4: `pregunta_04/diagrams/c4_security_architecture.drawio`
   - Ejercicio 5: `pregunta_05/diagrams/c4_observability_architecture.drawio`
   - Ejercicio 7: `pregunta_07/diagrams/cqrs_mediator_architecture.drawio`
3. *Método Alternativo*: En Draw.io ve a **Organizar -> Insertar -> Avanzado -> Mermaid** y pega el contenido del archivo `.mmd` correspondiente.
