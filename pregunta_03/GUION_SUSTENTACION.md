# Guión de Sustentación para Cámara - Ejercicio 3: Arquitectura en Tiempo Real

**Formato**: Guión para video de presentación / Entrevista técnica en vivo  
**Rol**: Arquitecto Senior de Software  
**Metodología**: **Why-Driven Design (WDD)** + **Modelo C4**  
**Duración Estimada**: 4 a 5 minutos  

---

## 🎬 ESCENA 1: MARCO METODOLÓGICO Y ANALOGÍA DE UBER (0:00 - 1:00)

**[Mirada directa a la cámara, postura firme y pausada]**

> **"Hola a todos.**
> 
> Presento la solución al **Ejercicio 3: Arquitectura en Tiempo Real para el Monitoreo de Emisión, Inspección y Siniestros**.
> 
> Para entender el diseño de forma muy sencilla, apliquemos la **analogía de la aplicación de Uber o Domino's Pizza Tracker**:
> 
> - Cuando pides un viaje o una pizza, la pantalla te muestra en tiempo real *"Preparando"*, *"Conductor asignado"* y *"En camino"*.
> - La aplicación **nunca recarga la página** a cada segundo (Short Polling), porque tumbaría los servidores. En su lugar, el servidor establece un canal directo (Server-Sent Events / SignalR) y **empuja (*PUSH*) la novedad** en milisegundos cuando **Apache Kafka** detecta el evento.
> 
> Bajo la metodología **Why-Driven Design (WDD)**, justificamos este diseño para eliminar el tráfico innecesario en la base de datos y ofrecer una experiencia instantánea al cliente."

---

## 🔍 ESCENA 2: MODELO C4 Y APACHE KAFKA BACKBONE (1:00 - 2:30)

**[Mostrar el diagrama C4 en pantalla o referenciar el archivo `.drawio`]**

> **"En el Diagrama de Contenedores Modelo C4 que he diseñado para Draw.io, la arquitectura se divide en 3 capas:**
> 
> 1. **Capa de Eventos (Apache Kafka)**: Los sistemas core de Emisión, Inspección y Siniestros publican sus novedades en tópicos independientes de Kafka. Kafka garantiza el orden estricto de eventos por cliente.
> 2. **Real-Time Gateway (SignalR / SSE Hub)**: Un microservicio especializado consume los eventos de Kafka y los transmite de forma no bloqueante a los navegadores.
> 3. **Redis Pub/Sub Backplane**: Para escalar horizontalmente el Gateway en múltiples servidores, Redis sincroniza los hubs de SignalR permitiendo atender a cientos de miles de usuarios en paralelo."

---

## ⚖️ ESCENA 3: DISCUSIÓN RIGUROSA DE TRADE-OFFS (2:30 - 4:00)

**[Tono analítico evaluando WebSockets, SignalR, SSE y Polling]**

> **"La evaluación nos exige analizar los Trade-offs de cada opción tecnológica:**
> 
> - **Server-Sent Events (SSE)**: Es nuestra opción recomendada para el dashboard de seguros. Utiliza la conexión HTTP/2 nativa del navegador, reconecta automáticamente y atraviesa firewalls sin problemas. Al ser un flujo unidireccional (Server->Client), es extremadamente liviano.
> - **SignalR (.NET Core)**: Es la mejor abstracción para ecosistemas .NET. Negocia automáticamente el transporte (WebSockets -> SSE -> Long Polling) y utiliza Redis Backplane para escalado distribuido.
> - **WebSockets**: Ofrece comunicación bi-direccional Full-Duplex TCP. Sin embargo, su trade-off es que requiere mantener estado (*Stateful*), exigiendo Redis Backplane o Sticky Sessions para balancear la carga.
> - **Short Polling**: Es un **antipatrón en tiempo real**. El 95% de las peticiones devuelven datos repetidos, desperdiciando CPU y ancho de banda. Solo se justifica en clientes legacy donde no exista otra opción."

---

## 🎯 ESCENA 4: CONCLUSIÓN Y DEMOSTRACIÓN (4:00 - 4:30)

> **"En conclusión: combinar Apache Kafka en el backbone con Server-Sent Events y SignalR en la frontera nos da una arquitectura en tiempo real capaz de escalar a millones de eventos con latencias menores a 10 milisegundos.**
> 
> Todo el código funcional, la prueba interactiva en Podman, la guía de Kubernetes y los diagramas C4 para Draw.io están listos en la carpeta `pregunta_03/`. ¡Muchas gracias!"**
