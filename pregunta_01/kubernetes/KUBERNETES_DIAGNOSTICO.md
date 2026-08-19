# Guía de Diagnóstico Paso a Paso en Kubernetes (Explicación Accesible)

## 📌 ¿Qué estamos buscando en Kubernetes?
Queremos confirmar con comandos sencillos que la API REST **no está usando el procesador (CPU)** ni **la memoria (RAM)**, sino que sus peticiones están **esperando en cola (I/O Wait)**.

---

## 1. Confirmar que el Servidor no está Cansado (Uso de Recursos)

```bash
# 1.1 Ver cuánto procesador y memoria está consumiendo cada Pod en tiempo real
kubectl top pods -l app=api-rest-service --containers
```
* **¿Qué esperamos ver?**: CPU < 10% y RAM < 30%. Esto nos demuestra que el pod no necesita más CPU ni está saturado.

---

## 2. Inspeccionar la Fila de Espera (Conexiones TCP)

```bash
# 2.1 Ver las conexiones abiertas dentro del Pod hacia el sistema externo
kubectl exec -it $(kubectl get pod -l app=api-rest-service -o jsonpath='{.items[0].metadata.name}') -- netstat -tan | grep 8080
```
* **¿Qué esperamos ver?**: Muchas conexiones en estado `ESTABLISHED` retenidas hacia el puerto del servicio externo. Esto confirma que la aplicación se quedó escuchando al teléfono esperando respuesta.

---

## 3. Tomar una "Fotografía" del Estado de los Hilos (Thread Dump)

```bash
# 3.1 Ver qué está haciendo el código dentro del Pod en este instante
kubectl exec -it $(kubectl get pod -l app=api-rest-service -o jsonpath='{.items[0].metadata.name}') -- py-spy dump --pid 1
```
* **¿Qué esperamos ver?**: Veremos que los hilos dicen literalmente **`WAITING` (Esperando)** o `SocketRead`. No están ejecutando código; están dormidos esperando datos de red.

---

## 4. Proyectar en Pantalla las Métricas de Latencia P95 (Prometheus / Grafana)

Consulta PromQL para mostrar la latencia P95 en pantalla durante la sustentación:

```promql
# Latencia P95 del servicio
histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket{app="api-rest-service"}[5m])) by (le))
```
* **Conclusión**: La gráfica mostrará una línea en **8 segundos**, confirmando la problemática.
