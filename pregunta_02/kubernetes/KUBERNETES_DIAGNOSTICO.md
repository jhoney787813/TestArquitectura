# Guía de Diagnóstico y Resiliencia en Kubernetes (Ejercicio 2)

## 📌 Diagnóstico de Resiliencia y Manejo de Fallas en Kubernetes

En esta arquitectura basamos la resiliencia de la emisión de pólizas en el desacoplamiento mediante el **Transactional Outbox Pattern** y **Workers Asíncronos**.

---

## 1. Verificar Salud de los Pods API y Workers

```bash
# Comprobar que los Pods de la API y los Workers están activos y listos
kubectl get pods -l 'app in (policy-api, notification-worker)' -o wide
```

---

## 2. Monitorear el Procesamiento de Notificaciones en Vivo

```bash
# Ver el consumo asíncrono de eventos desde los Workers
kubectl logs -l app=notification-worker --tail=100 -f | grep -E "EMAIL|SMS|AUDIT|DLQ"
```

---

## 3. Auditar la Dead Letter Queue (DLQ) en Caso de Fallas Persistentes

Cuando el proveedor de Email o SMS cae de manera prolongada, los eventos no se pierden; se mueven a la DLQ para su inspección y reintento manual:

```bash
# Inspeccionar eventos en DLQ dentro del Pod Worker
kubectl exec -it $(kubectl get pod -l app=notification-worker -o jsonpath='{.items[0].metadata.name}') -- curl -s http://localhost:8090/api/v1/dlq
```

---

## 4. Verificar el Estado del Circuit Breaker en los Gateways

Para verificar si el circuito de SMS está `CLOSED` (normal) u `OPEN` (bloqueando tráfico fallido):

```bash
kubectl exec -it $(kubectl get pod -l app=mock-gateways -o jsonpath='{.items[0].metadata.name}') -- curl -s http://localhost:8091/health
```
