# Guión de Sustentación para Cámara - Ejercicio 7: Patrón CQRS y Mediator (.NET 9)

**Formato**: Guión para video de presentación / Entrevista técnica en vivo  
**Rol**: Arquitecto Senior de Software  
**Enfoque**: Metodología **Why-Driven Design (WDD)**, **Clean Architecture (.NET 9)**, **CQRS**, **Patrón Mediator (MediatR)** y Atributos ISO 25010  
**Duración Estimada**: 4 a 5 minutos  

---

## 🎬 ESCENA 1: MARCO METODOLÓGICO Y LA ANALOGÍA DEL RESTAURANTE (0:00 - 1:15)

**[Mirada directa a la cámara, postura firme, analítica y profesional]**

> **"Hola a todos.**
> 
> Presento la solución al **Ejercicio 7: Arquitectura CQRS y Patrón Mediator en .NET 9**.
> 
> Para entender la potencia de esta arquitectura, apliquemos la **analogía de la Cocina del Restaurante**:
> 
> - **Queries (Lecturas - El Mesero con la Carta Impresa)**: Cuando un cliente pregunta qué platos hay disponibles, el mesero consulta la carta impresa (**Read Model / Redis Cache**) y responde de inmediato en milisegundos sin ir a molestar al Chef.
> - **Commands (Escrituras - El Chef en la Cocina)**: Cuando un cliente ordena un plato, la comanda entra al **Mediador (Command Bus)**. El Chef (**CommandHandler**) valida insumos (**ValidationBehavior**), ejecuta la receta con reglas estrictas de cocina y modifica el estado del inventario (**Write DB**).
> - **El Patrón CQRS + Mediator**: Separa la consulta rápida de la preparación compleja, permitiendo atender 10 veces más volumen de operaciones por segundo."

---

## 🔍 ESCENA 2: ARQUITECTURA DE LA SOLUCIÓN EN .NET 9 (1:15 - 2:30)

**[Tono estructurado evaluando los componentes de la solución]**

> **"Nuestra solución implementa Clean Architecture en .NET 9 dividiendo el sistema en dos pilas independientes:**
> 
> 1. **Command Stack (Escritura)**: Procesamos comandos como `CreatePolicyCommand` y `EmitPolicyCommand`. Ejecutan transacciones ACID en el modelo de escritura normalizado (PostgreSQL / SQL Server) y emiten eventos de dominio.
> 2. **Query Stack (Lectura)**: Procesamos consultas como `GetPolicyByIdQuery`. Leen directamente proyecciones DTO denormalizadas desde Redis o Réplicas de Lectura en menos de 2 milisegundos, bypaseando la sobrecarga de las entidades de dominio.
> 3. **Patrón Mediator (MediatR Bus)**: Elimina el acoplamiento directo entre los controladores y la lógica de negocio."

---

## 📊 ESCENA 3: PIPELINE BEHAVIORS EN MEDIATR (2:30 - 3:45)

**[Mostrar el diagrama C4 o explicar los Pipeline Behaviors]**

> **"Una de las mayores ventajas del patrón Mediator en .NET 9 son los Pipeline Behaviors (Cross-Cutting Concerns):**
> 
> - **`ValidationBehavior`**: Valida automáticamente las reglas de FluentValidation antes de tocar el handler. Si hay fallos, responde con `HTTP 422 Unprocessable Entity`.
> - **`LoggingAndPerformanceBehavior`**: Registra la entrada y salida de cada mensaje con su `TraceId` W3C y mide la latencia para Prometheus.
> - **`UnhandledExceptionBehavior`**: Captura excepciones no controladas y las convierte en formato estándar **RFC 7807 (ProblemDetails)**."

---

## 🎯 ESCENA 4: CONCLUSIÓN Y DEMOSTRACIÓN (3:45 - 4:30)

> **"En conclusión: la adopción de CQRS y Mediator en .NET 9 nos permite escalar de forma independiente las consultas de alta demanda sin poner en riesgo la consistencia de las escrituras de negocio.**
> 
> Todo el código funcional, la prueba interactiva en Podman en el puerto 8007, los diagramas C4 Model para Draw.io y la guía de Kubernetes están listos en la carpeta `pregunta_07/`. ¡Muchas gracias!"**
