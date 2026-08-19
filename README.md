# Test de Arquitectura de Software - Proceso de Selección Senior

**Postulante**: Jhon E. / Arquitecto Senior de Software  
**Repositorio Oficial**: [`https://github.com/jhoney787813/TestArquitectura`](https://github.com/jhoney787813/TestArquitectura)  
**Metodología de Arquitectura**: **Why-Driven Design (WDD)** | **Modelo C4** | **Clean Architecture (.NET 9)** | **CQRS & Mediator** | **ISO/IEC 25010**  

> 📑 **¿Buscas el desglose completo de enlaces, guiones y playbooks de Kubernetes?**  
> Consulta el **[ÍNDICE GENERAL Y DOCUMENTACIÓN COMPLETA DEL EXAMEN (`INDICE_GENERAL_EXAMEN.md`)](INDICE_GENERAL_EXAMEN.md)**.

---

## 📌 Resumen Ejecutivo para el Comité Evaluador

Este repositorio contiene la solución práctica, documentada y desplegable del **Examen Técnico de Arquitectura de Software (`Prueba Técnica - FWK Architect.docx`)**. 

Cada uno de los **7 Ejercicios Propuestos** está implementado como un proyecto ejecutable en contenedores OCI (Podman / Docker), con justificación técnica **Why-Driven Design (WDD)**, diagramas NATIVOS para Draw.io (`.drawio` XML y `.mmd` Mermaid) y playbooks operacionales de Kubernetes.

---

## 📊 Matriz Resumen de los 7 Ejercicios de la Prueba Técnica

| Ejercicio | Desafío de Arquitectura | Patrón / Solución Técnica | Justificación Técnica | Diagrama Draw.io Nativo | Demo Ejecutable |
| :---: | :--- | :--- | :---: | :---: | :---: |
| **01** | Diagnóstico de Performance (P95 = 8s) | Identificación de I/O Wait y Connection Pool Exhaustion *(Ventanillas del Banco)* | [`JUSTIFICACION.md`](pregunta_01/JUSTIFICACION_TECNICA.md) | N/A (I/O Wait) | `./run_visual_demo.sh` *(Caída a 15ms)* |
| **02** | Resiliencia y Outbox (Emisión de Póliza) | Transactional Outbox Pattern + Circuit Breaker + OpenSearch *(Tiquete de Avión)* | [`JUSTIFICACION.md`](pregunta_02/JUSTIFICACION_TECNICA.md) | [`component.drawio`](pregunta_02/diagrams/component_architecture.drawio) | `./run_visual_demo.sh` *(Escenarios A-E)* |
| **03** | Real Time (Emisión, Inspección, Siniestros) | Apache Kafka Event Backbone + SSE Gateway + Redis Pub/Sub *(Uber Tracker)* | [`JUSTIFICACION.md`](pregunta_03/JUSTIFICACION_TECNICA.md) | [`c4_realtime.drawio`](pregunta_03/diagrams/c4_model_realtime_architecture.drawio) | `./run_visual_demo.sh` *(SSE Stream)* |
| **04** | Auth & Revocación (REST, SOAP & WS) | OAuth 2.0 / JWT RS256 + Redis Token Blacklist TTL < 1ms *(Pasaporte e Interpol)* | [`JUSTIFICACION.md`](pregunta_04/JUSTIFICACION_TECNICA.md) | [`c4_security.drawio`](pregunta_04/diagrams/c4_security_architecture.drawio) | Web Client `http://localhost:8084` |
| **05** | Observability (Diagnóstico catch Exception) | OpenTelemetry W3C Tracing + Prometheus + Richardson Model + RFC 7807 *(Caja Negra)* | [`JUSTIFICACION.md`](pregunta_05/JUSTIFICACION_TECNICA.md) | [`c4_observability.drawio`](pregunta_05/diagrams/c4_observability_architecture.drawio) | `./run_visual_demo.sh` |
| **06** | Performance Engineering (100 ──► 500 TPS) | Métricas RED/USE + Async I/O + Redis Caching > 85% Hit Ratio + CQRS Read Replicas | [`JUSTIFICACION.md`](pregunta_06/JUSTIFICACION_TECNICA.md) | N/A (Escalado 5x) | Resumen Ejecutivo |
| **07** | Patrón CQRS y Mediator en .NET 9 | Clean Architecture .NET 9 + MediatR 12 + Pipeline Behaviors *(Cocina Restaurante)* | [`JUSTIFICACION.md`](pregunta_07/JUSTIFICACION_TECNICA.md) | [`cqrs_mediator.drawio`](pregunta_07/diagrams/cqrs_mediator_architecture.drawio) | `./run_visual_demo.sh` |

---

## 🚀 Guía Rápida de Ejecución en Podman / Docker

```bash
# Para probar cualquiera de los 7 ejercicios (ejemplo Ejercicio 7):
cd pregunta_07
podman compose up -d --build
./load_test/run_visual_demo.sh
```

---
*Para acceder al desglose de scripts de video, sustentaciones ante cámara y playbooks de Kubernetes, consulte la **[Documentación Completa (`INDICE_GENERAL_EXAMEN.md`)](INDICE_GENERAL_EXAMEN.md)**.*
