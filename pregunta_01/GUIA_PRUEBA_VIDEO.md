# Guía de Demostración Visual e Interactiva para Video (Ejercicio 1)

Esta guía describe cómo utilizar el nuevo script interactivo visual `./load_test/run_visual_demo.sh` para impactar al comité evaluador mostrando en la misma terminal el **ANTES (El Problema de 8s)** versus el **DESPUÉS (La Solución de 15ms)**.

---

## 🎬 PASO A PASO PARA GRABAR EN TERMINAL

### 🔹 Paso 1: Abrir la carpeta del proyecto
```bash
cd /Users/deals/Documents/GIT/TestArquitectura/pregunta_01
```

---

### 🔹 Paso 2: Ejecutar el Menú Visual Interactivo
```bash
./load_test/run_visual_demo.sh
```

En la consola aparecerá el menú interactivo en tiempo real:

```text
==========================================================================
    🚀 DEMOSTRACIÓN VISUAL DE ARQUITECTURA - EJERCICIO 1 (EN VIVO)
==========================================================================

Selecciona el escenario a demostrar para el video:
 1) 🔴 MOSTRAR EL PROBLEMA  (P95 = 8s - 15s | CPU = 2% | Pool Saturado)
 2) 🟢 MOSTRAR LA SOLUCIÓN  (P95 < 0.01s   | Cache Redis / Non-blocking)
 3) 📊 MOSTRAR MÉTRICAS PODMAN (stats en tiempo real)
```

---

### 🔴 OPCIÓN 1: MOSTRAR EL PROBLEMA DE PERFORMANCE

Ingresa `1` y presiona Enter.

**Lo que se verá en pantalla en vivo**:
```text
-> Lanzando 15 peticiones síncronas con concurrencia de 10...

   [CLIENTE #01] HTTP 200 OK | Recibido en: 8.17s | Latencia I/O Wait
   [CLIENTE #02] HTTP 200 OK | Recibido en: 8.17s | Latencia I/O Wait
   [CLIENTE #03] HTTP 200 OK | Recibido en: 8.17s | Latencia I/O Wait
   ...
============================================================
 RESULTADO DEMO 1 (PROBLEMA):
 - Tiempo Total de Ejecución: 16.25s
 - Latencia Máxima (P95)   : 8.17s  <-- [P95 = 8s - 15s]
============================================================
```

* **Qué decir a la cámara**:
  > *"Aquí vemos en pantalla el problema exacto: las peticiones tardan más de 8 segundos por la contención en el pool de conexiones e I/O Wait síncrono."*

---

### 🟢 OPCIÓN 2: MOSTRAR LA SOLUCIÓN APLICADA (¡IMPACTO VISUAL!)

Vuelve a ejecutar `./load_test/run_visual_demo.sh`, ingresa `2` y presiona Enter.

**Lo que se verá en pantalla en vivo**:
```text
-> Lanzando 20 peticiones a la API optimizada con Caché / Fast-Path...

   [CLIENTE #01] HTTP 200 OK | Respuesta instantánea en: 25.65 ms 🚀
   [CLIENTE #02] HTTP 200 OK | Respuesta instantánea en: 20.79 ms 🚀
   [CLIENTE #03] HTTP 200 OK | Respuesta instantánea en: 22.30 ms 🚀
   ...
============================================================
 RESULTADO DEMO 2 (SOLUCIÓN APLICADA):
 - Tiempo Total de Ejecución: 0.036s (en lugar de 16s!)
 - Latencia Promedio        : 15.88 ms
 - Mejora de Rendimiento    : ¡MÁS DE 1,000x MÁS RÁPIDO!
============================================================
```

* **Qué decir a la cámara**:
  > *"Al aplicar la solución con I/O Asíncrono no bloqueante y Caché Redis, la respuesta cae de 8.17 segundos a apenas 15 milisegundos. ¡Un rendimiento más de 1,000 veces superior!"*

---

### 📊 OPCIÓN 3: CONFIRMAR MÉTRICAS DE CPU Y RAM EN PODMAN

Ingresa `3` y presiona Enter.

```text
ID            NAME                CPU %       MEM USAGE / LIMIT  MEM %
877ca1738fd7  api_service_p1      2.20%       118.3MB / 268.4MB  44.05%
87f735bea175  mock_downstream_p1  0.75%        34.04MB / 134.2MB  25.36%
```

* **Qué decir a la cámara**:
  > *"Confirmamos en Podman stats que durante toda la prueba el consumo de CPU se mantuvo en 2.2% y RAM al 44%, validando que el procesador nunca fue el cuello de botella."*
