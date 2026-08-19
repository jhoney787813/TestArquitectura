# Guión de Sustentación para Cámara - Ejercicio 2 (Metodología Why-Driven Design)

**Formato**: Guión para video de presentación / Entrevista técnica en vivo  
**Rol**: Arquitecto Senior de Software  
**Enfoque**: Metodología **Why-Driven Design (WDD)**, Atributos de Calidad ISO 25010 y Trade-offs  
**Duración Estimada**: 4 a 5 minutos  

---

## 🎬 ESCENA 1: MARCO METODOLÓGICO WHY-DRIVEN DESIGN (0:00 - 1:00)

**[Mirada directa a la cámara, postura firme, segura y profesional]**

> **"Hola a todos.**
> 
> Para abordar el **Ejercicio 2: Patrones, Escalabilidad y Resiliencia en la Emisión de Pólizas**, sustento mi propuesta bajo la metodología **Why-Driven Design (WDD)**.
> 
> Como Arquitecto, la metodología WDD me exige no empezar por la tecnología, sino justificar cada decisión respondiendo a 3 preguntas fundamentales:
> 
> 1. **Business WHY**: ¿Por qué es crítica esta arquitectura? Porque emitir la póliza es el flujo principal de ingresos de la aseguradora. Ninguna falla externa debe cancelar una venta.
> 2. **Quality Attribute WHY**: ¿Por qué priorizamos latencia < 50ms y tolerancia a fallos? Porque el cliente exige confirmación de compra inmediata en su pantalla.
> 3. **Design WHY**: ¿Por qué elegimos el patrón **Transactional Outbox**? Porque desacopla el núcleo transaccional de los efectos secundarios propensos a fallos.
> 
> Usando la **analogía del tiquete de avión**: la reserva y el cobro se confirman de inmediato en la base de datos (**ACID**); si el correo con el tiquete en PDF o el SMS tardan unos segundos o fallan, **tu viaje no se cancela**."

---

## 🔍 ESCENA 2: RESPUESTA WDD A LAS PREGUNTAS A, B, C, D Y E (1:00 - 3:00)

**[Tono técnico riguroso, estructurado y claro]**

> **"Analicemos cada escenario bajo la metodología WDD:**
> 
> **A) El Diseño conveniente (Transactional Outbox + EDA):**
> Guardamos la póliza, la auditoría local y el evento Outbox en una **única transacción ACID local**. Respondemos al usuario en **0.2 milisegundos**. Un worker asíncrono procesa los envíos en segundo plano.
> 
> **B) ¿Qué pasa si `SavePolicy` falla?**
> Al ser la entidad núcleo de negocio, se ejecuta un **Rollback ACID completo**. Ningún registro se guarda, ningún evento Outbox se genera y ningún correo/SMS se envía. El sistema se mantiene 100% consistente.
> 
> **C) ¿Qué pasa si `SendEmail` falla?**
> La póliza **ya quedó emitida y garantizada**. El worker asíncrono ejecuta reintentos con *Exponential Backoff*. Si el servidor SMTP sigue caído, el mensaje se envía a la **Dead Letter Queue (DLQ)** para reintento operacional.
> 
> **D) ¿Qué pasa si SMS está caído?**
> El gateway implementa un **Circuit Breaker**. Si detecta fallas consecutivas, commuta a estado `OPEN` para cortar el tráfico (*fail-fast*) y desvía la notificación hacia un **Fallback** Push. La emisión de la póliza jamás se afecta.
> 
> **E) ¿Qué pasa si Audit falla y dónde persistir?**
> Aplicamos **Auditoría Dual**: una auditoría local ACID en la misma BD de la póliza y una auditoría centralizada en **ElasticSearch / OpenSearch** por su inmutabilidad *Append-Only* y velocidad de búsqueda JSON. Si OpenSearch cae, la auditoría local preserva la verdad legal y el evento reintenta en cola."

---

## ⚖️ ESCENA 3: ATRIBUTOS DE CALIDAD ISO 25010 Y MATRIZ DE TRADE-OFFS (3:00 - 4:00)

**[Demostrar madurez de arquitectura justificando compromisos implícitos]**

> **"Toda arquitectura profesional implica aceptar Trade-offs (Compromisos):**
> 
> - **Teorema CAP (Consistencia vs Disponibilidad)**: Aceptamos **Consistencia Eventual de segundos en notificaciones** a cambio de responder en milisegundos y garantizar 99.99% de disponibilidad en las ventas de pólizas.
> - **Atributo ISO 25010 de Tolerancia a Fallos**: Aceptamos mayor complejidad de infraestructura (administrar workers y colas DLQ) a cambio de aislar completamente el core del negocio de caídas en proveedores de terceros.
> - **Dual Audit Storage**: Aceptamos un costo marginal de almacenamiento en BD local a cambio de garantizar cero pérdida de trazas regulatorias."

---

## 🎯 ESCENA 4: CONCLUSIÓN Y CIERRE (4:00 - 4:30)

**[Cierre firme y profesional]**

> **"En resumen: con la metodología Why-Driven Design justificamos que cada patrón y cada mecanismo de resiliencia protegen el negocio, garantizan atributos de calidad ISO 25010 y optimizan la experiencia del cliente.**
> 
> Todo el código funcional, las pruebas en Podman y la documentación detallada están disponibles en la carpeta `pregunta_02/`. ¡Muchas gracias!"**
