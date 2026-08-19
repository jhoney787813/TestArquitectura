# Sustentación Técnica - Ejercicio 7: Patrón CQRS y Mediator en .NET 9

**Rol**: Arquitecto Senior de Software / Arquitecto de Soluciones  
**Metodología de Arquitectura**: **Why-Driven Design (WDD)**  
**Enfoque Central**: CQRS (Command Query Responsibility Segregation), Patrón Mediator (MediatR in .NET 9), Pipeline Behaviors, Modelos de Lectura/Escritura Separados y Consistencia Eventual  
**Diagramas C4 para Draw.io**: [`diagrams/cqrs_mediator_architecture.drawio`](file:///Users/deals/Documents/GIT/TestArquitectura/pregunta_07/diagrams/cqrs_mediator_architecture.drawio)  
**Proyecto de Referencia**: `pregunta_07/`  

---

## 💡 1. Explicación Didáctica y Accesible (La Analogía de la Cocina del Restaurante)

> **Para explicar esta solución a cualquier audiencia:**
> 
> Imagine la dinámica de trabajo en un restaurante de alta cocina:
> 
> 1. **Queries (Lecturas - El Mesero con la Carta Impresa)**: Cuando un cliente consulta los platos disponibles, el mesero revisa la carta impresa (**Read Model / Redis Cache**) y responde de inmediato en milisegundos sin interrumpir al Chef.
> 2. **Commands (Escrituras - El Chef en la Cocina)**: Cuando un cliente ordena *"Preparar un filete a la pimienta"*, el pedido entra al **Mediador (Command Bus)**. El Chef (**CommandHandler**) valida los insumos (**ValidationBehavior**), ejecuta la receta aplicando reglas estrictas de cocina, altera el estado del inventario (**Write DB**) y publica el evento de que el plato está listo.
> 3. **El Patrón CQRS + Mediator**: Separa completamente la consulta rápida en sala de la preparación compleja en cocina, logrando que el restaurante atienda 10 veces más clientes por hora.

---

## 🎨 2. Modelo C4 de la Arquitectura CQRS & Mediator (C4 Level 2 - Container Diagram)

El siguiente diagrama en formato **C4 Model** representa la separación de capas y el bus de mensajes:

```mermaid
graph TB
    subgraph Users ["1. ACTORES Y PRESENTACIÓN"]
        User["Persona: Cliente / API Client<br>Envía Commands (Modificaciones) y Queries (Consultas)"]
    end

    subgraph SystemBoundary ["2. C4 SYSTEM BOUNDARY: ARQUITECTURA CQRS & PATRÓN MEDIATOR"]
        Mediator["Container: MediatR Mediator Bus (.NET 9)<br>(Pipeline Behaviors: ValidationBehavior & LoggingBehavior)"]
        
        subgraph WriteStack ["3. PILA DE ESCRITURA (COMMAND STACK - WRITE MODEL)"]
            CmdHandlers["Component: Command Handlers<br>(CreatePolicyCommandHandler & EmitPolicyCommandHandler)"]
            WriteDB[("Database: Master Write DB (PostgreSQL)<br>(Modelo Normalizado 3NF - ACID Transactions)")]
        end

        subgraph ReadStack ["4. PILA DE LECTURA (QUERY STACK - READ MODEL)"]
            QueryHandlers["Component: Query Handlers<br>(GetPolicyByIdQueryHandler & SummaryQueryHandler)"]
            ReadDB[("Database: Read Replicas / Redis Cache<br>(Proyecciones DTO Denormalizadas - Latencia < 2ms)")]
        end
    end

    User -->|Envía Requests HTTP| Mediator
    Mediator -->|Despacha Commands| CmdHandlers
    Mediator -->|Despacha Queries| QueryHandlers

    CmdHandlers -->|Persiste Entidades ACID| WriteDB
    QueryHandlers -->|Consultas DTO Directas| ReadDB

    WriteDB -.->|Sincronización Asíncrona (Eventual Consistency)| ReadDB

    classDef c4User fill:#08427b,stroke:#073866,fontColor:#ffffff;
    classDef c4Container fill:#1168bd,stroke:#0e5296,fontColor:#ffffff;
    classDef c4Db fill:#85bbf0,stroke:#0e5296,fontColor:#000000;
    classDef c4Producer fill:#2b7bba,stroke:#0e5296,fontColor:#ffffff;

    class User c4User;
    class Mediator,CmdHandlers,QueryHandlers c4Container;
    class WriteDB,ReadDB c4Db;
```

---

## 🎯 3. Marco Metodológico: Why-Driven Design (WDD)

Bajo **Why-Driven Design (WDD)**, justificamos la implementación de CQRS y Mediator respondiendo al **¿POR QUÉ?**:

1. **Business WHY**: Evitar la contención de base de datos cuando miles de usuarios consultan pólizas al mismo tiempo que los agentes emiten nuevas pólizas. Separa el modelo de lectura para soportar picos de consulta sin impactar las transacciones de negocio.
2. **Quality Attribute WHY (ISO 25010)**: Priorizamos **Eficiencia de Rendimiento** (Respuestas de lectura < 2ms), **Mantenibilidad** (Desacoplamiento total entre controladores y lógica de dominio) y **Escalabilidad** (Capacidad de escalar réplicas de lectura sin escalar el Master DB).
3. **Design WHY (Patrón Mediator in .NET 9)**: **MediatR** actúa como el bus in-memory que desacopla la capa de presentación de la capa de aplicación. Permite inyectar **Pipeline Behaviors** (Canalizaciones transversales) para validaciones, logging y transacciones sin duplicar código.
4. **Technology WHY**: **.NET 9 + MediatR 12.0** ofrece despachos de mensajes ultra-eficientes con asignaciones de memoria mínimas (*Allocation-free performance*).

---

## 🔍 4. Justificación Técnica de la Arquitectura Implementada

### A) ¿Por qué separar Commands y Queries (CQRS)?

En un diseño CRUD tradicional, una sola entidad de base de datos sirve para leer datos en la pantalla y para ejecutar transacciones ACID de negocio. Esto genera:
- **Sobrecarga de Lectura**: Mapear tablas complejas con 50 columnas para solo mostrar 3 campos en un listado web.
- **Bloqueos de Transacción (Lock Contention)**: Las lecturas masivas bloquean las escrituras de nuevas pólizas.

**Solución CQRS**:
- **Commands (Pila de Escritura)**: `CreatePolicyCommand`, `EmitPolicyCommand`. Modifican estado, aplican reglas de dominio ricas y garantizan consistencia ACID.
- **Queries (Pila de Lectura)**: `GetPolicyByIdQuery`, `GetPoliciesSummaryQuery`. Leen proyecciones denormalizadas directas DTO desde Redis / Réplicas de Lectura en < 2ms, bypaseando la complejidad de las entidades de dominio.

---

### B) ¿Por qué usar el Patrón Mediator (MediatR)?

El patrón **Mediator** elimina las dependencias directas entre los controladores de la API y los servicios de aplicación. El controlador solo sabe enviar un `IMessage` al Mediator Bus (`await _mediator.Send(command)`).

#### Pipeline Behaviors Implementados (.NET 9 Cross-Cutting Concerns):

```text
 Request ──► [ValidationBehavior] ──► [LoggingBehavior] ──► [UnhandledExceptionBehavior] ──► Handler Execution
```

1. **`ValidationBehavior`**: Intercepta comandos antes de su ejecución usando **FluentValidation**. Si existen errores de validación, detiene el pipeline y responde con `HTTP 422 Unprocessable Entity`.
2. **`LoggingBehavior`**: Registra la entrada y salida de cada Command/Query con su `TraceId` y tiempo de ejecución.
3. **`UnhandledExceptionBehavior`**: Captura excepciones no controladas y las formatea como **RFC 7807 ProblemDetails**.

---

## ⚖️ 5. Matriz de Trade-offs (Análisis de Compromisos)

| Aspecto | Arquitectura Monolítica CRUD | Solución Propuesta (CQRS + Mediator .NET 9) | Trade-off / Justificación WDD |
| :--- | :--- | :--- | :--- |
| **Mantenibilidad** | Pobre (Controladores acoplados a servicios) | Alta (Desacoplamiento total via MediatR Pipeline Behaviors) | **Compromiso**: Ligero incremento en el número de clases (Commands, Queries, Handlers) a cambio de arquitectura limpia. |
| **Rendimiento de Lectura** | Lento (Consultas a tablas normalizadas 3NF) | Ultra-rápido (< 2ms leyendo proyecciones denormalizadas) | **Compromiso**: Incurrimos en **Consistencia Eventual** (milisegundos) para actualizar la proyección de lectura. |
| **Escalabilidad** | Limitada por el nodo Master de BD | Alta (Escalado independiente de Réplicas de Lectura) | **Compromiso**: Requiere sincronización de eventos de dominio para actualizar la base de datos de lectura. |

---

## 🎯 6. Criterios de Calidad ISO/IEC 25010

1. **Eficiencia de Rendimiento**: Trazado y despacho de consultas en < 2ms utilizando proyecciones del *Read Model*.
2. **Mantenibilidad**: Adopción estricta de Principios SOLID (Single Responsibility y Dependency Inversion).
3. **Interoperabilidad**: Respuestas estandarizadas en formato JSON y cabeceras W3C TraceContext.
