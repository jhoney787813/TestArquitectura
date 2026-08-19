# Test de Arquitectura de Software - Proceso de Selección Senior

**Postulante**: Jhon E. / Arquitecto Senior de Software  
**Cuenta de GitHub**: [`jhoney787813`](https://github.com/jhoney787813)  
**Repositorio**: [`https://github.com/jhoney787813/TestArquitectura`](https://github.com/jhoney787813/TestArquitectura)  
**Metodología de Arquitectura**: **Why-Driven Design (WDD)** | **ISO/IEC 25010 Quality Attributes** | **Transactional Outbox & Resiliency Patterns**  

---

## 📌 Mensaje Dirigido al Comité Evaluador de Arquitectura

Estimado equipo evaluador y líderes técnicos del proceso de selección:

Este repositorio contiene la solución práctica, documentada y desplegable del **Examen Técnico de Arquitectura de Software (`Prueba Técnica - FWK Architect.docx`)**. 

A diferencia de propuestas puramente teóricas o conceptuales, cada ejercicio aquí presentado ha sido **construido como un proyecto funcional ejecutable en contenedores OCI (Podman / Docker)**, respaldado por **evidencia empírica en tiempo real**, **playbooks operacionales en Kubernetes**, **diagramas de componentes para Draw.io** y una **sustentación guiada por la metodología Why-Driven Design (WDD)**.

El objetivo de esta entrega es demostrar no solo el conocimiento de patrones avanzados de microservicios y resiliencia, sino la **experiencia práctica y *expertise* en el sector de arquitectura empresarial**, traduciendo decisiones técnicas complejas en valor de negocio medible, alta tolerancia a fallos y excelente comunicación técnica.

---

## 📂 Navegación Estructurada por Ejercicios

El repositorio se encuentra organizado de forma modular por carpetas independientes marcadas por cada pregunta (`pregunta_01/`, `pregunta_02/`, ...):

```text
TestArquitectura/
├── README.md                   # Presentación general para el equipo de selección
├── pregunta_01/                # Ejercicio 1: Diagnóstico de Performance (CPU 10%, RAM 30%, P95 8s)
│   ├── app/                    # REST API simulada con bloqueo I/O Wait
│   ├── mock_downstream/        # Servicio dependiente lento (8s)
│   ├── load_test/              # Pruebas de carga en vivo y consola visual coloreada
│   ├── kubernetes/             # Manifests Deployment/Service & Playbook kubectl
│   ├── JUSTIFICACION_TECNICA.md# Sustentación técnica con la Analogía de las Ventanillas del Banco
│   ├── GUION_SUSTENTACION.md   # Script listo para grabación ante cámara
│   └── GUIA_PRUEBA_VIDEO.md    # Manual ejecutable paso a paso para el video
│
└── pregunta_02/                # Ejercicio 2: Patrones, Escalabilidad y Resiliencia (Emisión de Pólizas)
    ├── app/                    # API REST con Transactional Outbox Pattern
    ├── workers/                # Worker asíncrono con Exponential Backoff y DLQ
    ├── mock_services/          # Gateways con Circuit Breaker (SMS) e ingesta OpenSearch Audit
    ├── load_test/              # Script CLI interactivo para probar Escenarios A, B, C, D y E
    ├── diagrams/               # Diagramas de Componentes (.drawio XML nativo y .mmd Mermaid)
    ├── kubernetes/             # Manifests K8s & Comandos de verificación de resiliencia
    ├── JUSTIFICACION_TECNICA.md# Sustentación Why-Driven Design (WDD) & ISO 25010
    ├── GUION_SUSTENTACION.md   # Script para cámara con la Analogía del Tiquete de Avión
    └── GUIA_PRUEBA_VIDEO.md    # Manual de demostración en vivo
```

---

## 🛠️ Resumen de Ejercicios y Soluciones Técnicas

### 🔴 Ejercicio 1: Diagnóstico de Performance (CPU 10%, RAM 30%, P95 = 8s)
- **Problemática**: Una API REST consume solo 10% de CPU y 30% de RAM, pero su latencia P95 se dispara a 8 segundos.
- **Diagnóstico del Arquitecto**: Se descarta falta de procesador o memory leak. El sistema sufre de **I/O Wait / Thread Pool Starvation / Connection Pool Exhaustion**. Los hilos están en estado `WAITING` retenidos en sockets de red.
- **Demostración Práctica**: En `pregunta_01/` se despliega la API en Podman y se ejecuta `./load_test/run_visual_demo.sh`. Se comprueba empíricamente CPU al ~2%, RAM al ~44% y latencia de 8.17s.
- **Solución Aplicada**: En la misma consola se demuestra la opción optimizada con I/O Asíncrono no bloqueante y Caché Redis, **reduciendo la latencia de 8.17s a solo 15 milisegundos (>1,000x más rápido)**.
- **Documentos Clave**:
  - [Justificación Técnica Ejercicio 1](pregunta_01/JUSTIFICACION_TECNICA.md)
  - [Guión para Cámara - Analogía del Banco](pregunta_01/GUION_SUSTENTACION.md)
  - [Guía de Diagnóstico en Kubernetes](pregunta_01/kubernetes/KUBERNETES_DIAGNOSTICO.md)

---

### 🛡️ Ejercicio 2: Patrones, Escalabilidad y Resiliencia (Emisión de Póliza)
- **Problemática**: Diseñar la emisión de una póliza que requiere actualizar BD, enviar Email, enviar SMS y generar Auditoría, evaluando qué ocurre ante fallas en cada componente (Preguntas A, B, C, D y E).
- **Enfoque de Arquitectura**: **Metodología Why-Driven Design (WDD)** + **Transactional Outbox Pattern** + **Event-Driven Architecture (EDA)**.
- **Respuestas a los Escenarios Evaluados**:
  - **A) Diseño de Emisión**: Transacción ACID local guarda Póliza + Auditoría Local + Evento Outbox en la misma BD relacional. Respuesta HTTP al cliente en **< 50ms (0.23ms comprobado)**.
  - **B) Si `SavePolicy` falla**: **Rollback ACID completo**. Ninguna póliza se crea, ningún evento se genera, ningún email/SMS es enviado (Consistencia del 100%).
  - **C) Si `SendEmail` falla**: La Póliza **permanece emitida de forma segura**. El worker asíncrono reintenta con *Exponential Backoff* y desplaza el correo a la **Dead Letter Queue (DLQ)**.
  - **D) Si SMS está caído**: Un **Circuit Breaker** commuta a estado `OPEN` (*fail-fast*) y desvía la notificación hacia un **Fallback Push**. La emisión de la póliza jamás se bloquea.
  - **E) Si Audit falla & Persistencia**: **Auditoría Dual**. Auditoría local ACID en la BD relacional protege legalmente a la empresa. Auditoría centralizada en **ElasticSearch / OpenSearch** por inmutabilidad *Append-Only* y búsqueda JSON distribuida.
- **Documentos y Diagramas Clave**:
  - [Justificación WDD y Trade-offs ISO 25010](pregunta_02/JUSTIFICACION_TECNICA.md)
  - [Guión para Cámara - Analogía del Tiquete de Avión](pregunta_02/GUION_SUSTENTACION.md)
  - [Diagrama de Componentes NATIVO para Draw.io XML](pregunta_02/diagrams/component_architecture.drawio)
  - [Diagrama de Componentes Mermaid](pregunta_02/diagrams/component_architecture.mmd)

---

## 🚀 Guía Rápida de Ejecución Práctica en Podman / Docker

Para verificar el funcionamiento en vivo de cualquiera de los ejercicios en tu máquina local:

### Para probar el Ejercicio 1 (Diagnóstico de Performance):
```bash
cd pregunta_01
podman compose up -d --build
./load_test/run_visual_demo.sh
```

### Para probar el Ejercicio 2 (Resiliencia y Outbox Pattern):
```bash
cd pregunta_02
podman compose up -d --build
./load_test/run_visual_demo.sh
```

---

## 🎨 Cómo visualizar el Diagrama de Arquitectura en Draw.io

1. Abre **[app.diagrams.net](https://app.diagrams.net)** en tu navegador.
2. Haz clic en **Abrir diagrama existente** y selecciona el archivo de este repositorio:  
   `pregunta_02/diagrams/component_architecture.drawio`
3. O bien, en Draw.io ve a **Organizar -> Insertar -> Avanzado -> Mermaid** y pega el contenido del archivo `pregunta_02/diagrams/component_architecture.mmd`.

---

## 🎯 Criterios de Calidad y Compromisos (Trade-offs)

Bajo la norma **ISO/IEC 25010**, los proyectos destacan los siguientes compromisos asumidos:

- **Consistencia Eventual vs. Consistencia Fuerte Inmediata**: Aceptamos consistencia eventual de segundos en canales de notificación (Email/SMS) a cambio de garantizar la respuesta HTTP en milisegundos y un SLA de disponibilidad del 99.99%.
- **Tolerancia a Fallos vs. Complejidad Operativa**: Incurrimos en administrar workers asíncronos y colas DLQ a cambio de aislar completamente el core del negocio de caídas en proveedores de terceros.

---
*Repositorio creado y mantenido por Jhon E. para el proceso de selección de Arquitecto de Software.*
