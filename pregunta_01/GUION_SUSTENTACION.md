# Guión de Sustentación para Cámara - Ejercicio 1: Diagnóstico de Performance (Explicación Didáctica y Profesional)

**Formato**: Guión para video de presentación / Entrevista técnica en vivo  
**Rol**: Arquitecto Senior de Software  
**Estilo de Comunicación**: Claro, profesional, didáctico e intuitivo (fácil de entender para perfiles junior, gerenciales o técnicos).  
**Duración Estimada**: 4 a 5 minutos  

---

## 🎬 ESCENA 1: INTRODUCCIÓN Y LA ANALOGÍA DEL BANCO (0:00 - 1:00)

**[Mirada a la cámara, postura cercana, amable y profesional]**

> **"Hola a todos.**
> 
> Me presento a esta prueba de arquitectura para responder la primera pregunta: **¿Qué investigar si una API REST consume solo 10% de CPU, 30% de Memoria RAM, pero las respuestas tardan 8 segundos (P95 = 8s)?**
> 
> A primera vista, estos números parecen contradictorios. Para entenderlo de forma muy sencilla, imaginemos una **ventanilla de un banco**:
> 
> - **La CPU al 10%** significa que los cajeros del banco no están corriendo de un lado a otro ni están cansados. Tienen mucho tiempo libre.
> - **La RAM al 30%** significa que el banco está ordenado y no está lleno de cajas ni papeles amontonados.
> - **Sin embargo, la fila afuera del banco tarda 8 minutos (8 segundos en el sistema)**. ¿Por qué ocurre esto si los cajeros no están ocupados?
> 
> Ocurre porque **solo hay 5 ventanillas abiertas** y cada cajero está esperando una llamada telefónica lenta que tarda 8 segundos. Los clientes afuera no avanzan porque están **esperando su turno en la fila**, no porque el banco esté sobrecargado de trabajo.
> 
> En arquitectura de software, a esto lo llamamos **I/O Wait o Agotamiento de Pools de Conexión**: la aplicación no está procesando datos en el procesador; simplemente está **esperando con los brazos cruzados** a que un sistema externo o la base de datos le responda."

---

## 🔍 ESCENA 2: ¿QUÉ INVESTIGARÍAMOS EXACTAMENTE? (1:00 - 2:15)

**[Tono explicativo, usando un lenguaje estructurado sin jerga innecesaria]**

> **"Sabiendo esto, como Arquitecto no iría a comprar servidores más grandes ni a pedir más procesador. Investigaría 4 puntos clave:**
> 
> **1. El tamaño del Pool de Conexiones (La fila de espera):**
> ¿Cuántas peticiones permitimos procesar al mismo tiempo hacia la base de datos o el sistema externo? Si la capacidad es de 5 y llegan 100 personas, 95 personas tendrán que esperar en la cola sin consumir CPU.
> 
> **2. Dependencias Externas Lentas (El teléfono que no responde):**
> ¿La API está llamando a un sistema antiguo, un proveedor de pagos o un servicio de terceros que tarda 8 segundos en responder? Mientras ese sistema externo responde, nuestro sistema se queda 'esperando en la línea'.
> 
> **3. Bloqueos en la Base de Datos (Turnos trabados):**
> ¿Hay dos o más usuarios intentando modificar el mismo registro al mismo tiempo? Cuando esto pasa, la base de datos hace que el segundo usuario espere a que el primero termine.
> 
> **4. Filas en la Puerta de Entrada (Ingress / Red):**
> ¿Las peticiones se están acumulando en la puerta del servidor antes de poder entrar a la aplicación?"

---

## 💻 ESCENA 3: DEMOSTRACIÓN PRÁCTICA EN KUBERNETES (2:15 - 3:30)

**[Mostrar pantalla con la terminal o referenciar los comandos del proyecto]**

> **"Para mostrar esto en vivo en un entorno de Kubernetes, no necesitamos comandos complejos, sino seguir un camino lógico:**
> 
> 1. Primero, confirmamos que el servidor está tranquilo ejecutando `kubectl top pods`. Veremos que el uso de CPU es casi nulo.
> 2. Segundo, miramos cuántas personas están 'conectadas esperando' dentro del contenedor usando `kubectl exec netstat`. Veremos conexiones abiertas esperando respuesta.
> 3. Tercero, le tomamos una 'fotografía' a lo que están haciendo los hilos del programa (un *Thread Dump*). Allí confirmaremos literalmente que los hilos dicen el estado **`WAITING` (Esperando)**.
> 
> En nuestro proyecto simulado en Podman, dentro de la carpeta `pregunta_01/`, hemos incluido un script ejecutable llamado `run_test.sh` que reproduce exactamente este comportamiento en consola."

---

## 🛠️ ESCENA 4: ¿CÓMO LO SOLUCIONAMOS DE FORMA DEFINITIVA? (3:30 - 4:30)

**[Tono propositivo, orientado a soluciones de impacto]**

> **"La solución no es darle más CPU al servidor, sino reorganizar el flujo de trabajo:**
> 
> - **Paso 1 - Poner un límite de tiempo (Timeouts y Interruptor de Seguridad / Circuit Breaker):** Si el sistema externo tarda más de 2 segundos, no hacemos esperar al usuario 8 segundos. Cortamos la llamada y le mostramos un mensaje amable o un dato guardado en memoria.
> - **Paso 2 - Ampliar las ventanillas (Ajustar Connection Pools):** Darle suficiente capacidad al sistema para atender solicitudes simultáneas.
> - **Paso 3 - Usar un Buzón de Mensajes (Arquitectura Asíncrona):** Si una tarea tarda 8 segundos obligatoriamente (por ejemplo, generar un PDF o procesar un pago), no hacemos esperar al usuario en la pantalla. Le decimos *'Recibido, te avisamos cuando esté listo'* en menos de 100 milisegundos y procesamos la tarea por detrás con herramientas como Kafka o RabbitMQ.
> - **Paso 4 - Memoria Caché (Redis):** Si 1,000 personas piden la misma información lenta, la guardamos en una memoria rápida para responder en 5 milisegundos."

---

## 🎯 ESCENA 5: CONCLUSIÓN (4:30 - 5:00)

**[Cierre cálido, profesional y seguro]**

> **"En conclusión: un alto tiempo de respuesta con bajo uso de procesador y memoria no es un problema de potencia, sino un problema de espera y cola.**
> 
> Con este enfoque, demostramos que entendemos la causa raíz técnica, pero también sabemos cómo comunicarlo claramente a cualquier equipo para tomar las decisiones correctas.
> 
> Todo el código funcional, los manifests de Kubernetes y la documentación detallada están listos en la carpeta `pregunta_01/`. ¡Muchas gracias!"**
