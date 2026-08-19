# Sustentación Técnica - Ejercicio 6: Performance Engineering (Escalado de 100 a 500 TPS)

**Rol**: Arquitecto Senior de Software / Arquitecto de Soluciones  
**Metodología de Arquitectura**: **Why-Driven Design (WDD)**  
**Enfoque Central**: Métricas RED/USE, Diagnóstico de Cuellos de Botella, Caching Distribuido, CQRS y Escalado Horizontal  
**Caso de Estudio**: Incremento de capacidad transaccional de 100 TPS a 500 TPS (Escalado 5x)  

---

## 💡 1. Analogía Didáctica (El Peaje de la Autopista de 100 a 500 Vehículos/segundo)

> **Para explicar este desafío de rendimiento:**
> 
> Pasar de 100 TPS a 500 TPS en un peaje de autopista **no se logra simplemente contratando a 5 cajeros más (escalado vertical ciego)** si la barrera tarda 10 segundos en levantar (I/O Wait / BD bottleneck) o si hay una sola fila para pagar.
> 
> Primero medimos **dónde se forma la congestión (Métricas USE/RED)**; luego implementamos cobro electrónico automático por telepeaje (**Caching Redis & Asincronismo Outbox**) y finalmente abrimos más cabinas peajeras desacopladas (**Escalado Horizontal y Réplicas de Lectura BD**).

---

## 🔍 2. Respuesta Exhaustiva a las Preguntas A y B

### A) ¿Qué mediría primero? (Metodología de Diagnóstico de Performance)

Como Arquitecto de Software, **nunca escalamos a ciegas sin antes identificar el cuello de botella real (Bottleneck Analysis)**. Aplicaremos la metodología combinada **USE (Utilization, Saturation, Errors)** y **RED (Rate, Errors, Duration)**:

#### 1. Métricas RED del Servicio (Frontera de Entrada HTTP/gRPC):
* **Duration / Latency Distribution (Histograma P95, P99)**: Medir la distribución del tiempo de respuesta. Si el P95 es muy superior al promedio, indica contención en hilos o I/O bloqueante.
* **Throughput / Rate**: Validar la tasa real de 100 TPS y el porcentaje de errores (**Error Rate / HTTP 5xx**).

#### 2. Métricas USE de Infraestructura y Servidores:
* **I/O Wait & Disk IOPS**: Medir el porcentaje de tiempo que la CPU pasa esperando operaciones de disco o red (*el cuello de botella #1 en sistemas estancados en 100 TPS*).
* **Saturación del Connection Pool de Base de Datos**: Medir conexiones activas vs en espera (*Connection Pool Starvation*), tiempos de checkout de conexiones y consultas lentas (*Slow Query Log*).
* **Thread Pool Utilization / Starvation**: Medir si los hilos del servidor web se agotan por llamadas síncronas bloqueantes a servicios externos.
* **Garbage Collection (GC) Pauses**: Frecuencia y duración de pausas de Stop-the-World en la memoria RAM.

#### 3. Métricas de Base de Datos y Servicios Downstream:
* **Lock Contention / Table Locks**: Bloqueos y Deadlocks en transacciones ACID largas.
* **Latencia de Red Downstream**: Tiempos de respuesta de pasarelas de pago o APIs de terceros.

---

### B) ¿Cómo escalaría? (Plan de Escalado de 100 TPS a 500 TPS - Escalado 5x)

Para quintuplicar la capacidad (100 TPS -> 500 TPS), aplicamos un plan por capas guiado por el principio de **eficiencia de recursos y menor costo total de propiedad (TCO)**:

#### 1. Fase 1: Optimización de Código e I/O Bloqueante (Capacidad estimada: ~200 TPS)
* **Eliminar I/O Bloqueante (Async/Await E2E)**: Transformar todas las llamadas a Base de Datos y APIs remotas en operaciones asíncronas no bloqueantes para liberar hilos del servidor.
* **Optimización de Consultas SQL e Índices**:
  * Eliminar lecturas redundantes `SELECT *` y aplicar proyecciones específicas.
  * Crear índices compuestos basados en el plan de ejecución (`EXPLAIN ANALYZE`).
  * Evitar llamadas HTTP externas dentro de transacciones ACID de base de datos.

#### 2. Fase 2: Estrategia de Caching y Desacoplamiento (Capacidad estimada: ~350 TPS)
* **Caché Distribuido Multi-Nivel (Redis Cluster)**:
  * Cachear lecturas de alto volumen (datos maestros, catálogos, sesiones) usando el patrón **Cache-Aside** con TTL automatizado.
  * Alcanzar un *Cache Hit Ratio* > 85%, reduciendo el 80% de la carga sobre la base de datos relacional.
* **Desacoplamiento Asíncrono (Event-Driven Architecture / Outbox Pattern)**:
  * Procesar operaciones secundarias (envío de emails, SMS, auditoría, analítica) de forma asíncrona mediante colas de mensajes (**Apache Kafka / RabbitMQ**), respondiendo al cliente en < 20ms.

#### 3. Fase 3: Escalado de Arquitectura y Base de Datos (Capacidad alcanzada: 500+ TPS)
* **Segregación de Lectura/Escritura (CQRS & Read Replicas)**:
  * Dirigir escrituras (10-20% del tráfico) al nodo primario (Master BD).
  * Dirigir lecturas (80-90% del tráfico) a **Réplicas de Lectura (Read Replicas)** distribuidas con balanceo de carga.
* **Connection Pooling & Proxy de BD (pgBouncer / ProxySQL)**:
  * Reutilizar conexiones activas de base de datos mediante un proxy de conexiones para eliminar la sobrecarga de apertura/cierre de sockets TCP.
* **Escalado Horizontal Autoscaling en Kubernetes (HPA)**:
  * Configurar **Horizontal Pod Autoscaler (HPA)** en K8s aumentando dinámicamente las réplicas del microservicio basado en métricas de latencia P95 y CPU (> 70%).

---

## 📑 Resumen Ejecutivo del Arquitecto (Executive Summary)

```text
 ┌────────────────────────────────────────────────────────────────────────────────────────┐
 │                     HOJA DE RUTA DE ARQUITECTURA: 100 TPS ──► 500 TPS                  │
 ├──────────────────────────┬───────────────────────────┬─────────────────────────────────┤
 │ 1. DIAGNÓSTICO (MEDIR)   │ 2. OPTIMIZACIÓN ENTRADA   │ 3. ESCALADO ESTRUCTURAL         │
 │ • Métricas RED & USE     │ • Async/Await I/O         │ • Redis Caching (Hit > 85%)     │
 │ • Latencia P95 / P99     │ • Índices SQL & Explains  │ • CQRS & Read Replicas BD       │
 │ • Connection Pool BD     │ • DB Proxy (pgBouncer)    │ • K8s Autoscaling (HPA)         │
 └──────────────────────────┴───────────────────────────┴─────────────────────────────────┘
```

> **Conclusión de Arquitectura:**
> Quintuplicar la capacidad de 100 a 500 TPS no requiere multiplicar por 5 el costo de los servidores. Se logra combinando **eficiencia en I/O asíncrono**, **caching distribuido en Redis** para absorber el 80% de las lecturas, **segregación de réplicas de lectura (CQRS)** y **autoscaling horizontal en Kubernetes**. 
> 
> Esta estrategia garantiza alcanzar los 500 TPS manteniendo latencias P95 inferiores a 50 ms y un costo de infraestructura optimizado.
