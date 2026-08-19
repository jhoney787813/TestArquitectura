# Guía de Diagnóstico de Tiempo Real en Kubernetes (Ejercicio 3)

## 📌 Verificación de Conexiones Persistentes (SSE & WebSockets) en K8s

En Kubernetes, mantener conexiones persistentes en tiempo real (WebSockets / SSE) requiere un manejo cuidadoso de los **timeouts de Ingress (ingress-nginx / Istio)** y la sincronización entre réplicas mediante un **Redis Backplane**.

---

## 1. Verificar Estado del Real-Time Gateway y Suscriptores Activos

```bash
# Consultar el número de suscriptores SSE y WebSockets activos dentro del Pod
kubectl exec -it $(kubectl get pod -l app=realtime-api -o jsonpath='{.items[0].metadata.name}') -- curl -s http://localhost:8000/health
```

---

## 2. Probar Transmisión SSE Continua desde Consola

```bash
# Conectarse al stream HTTP SSE (-N evita buffering en curl)
kubectl exec -it $(kubectl get pod -l app=realtime-api -o jsonpath='{.items[0].metadata.name}') -- curl -N http://localhost:8000/api/v1/realtime/stream
```

---

## 3. Configuración Requerida en Ingress NGINX para WebSockets & SSE

Para evitar que NGINX Ingress cierre las conexiones persistentes tras 60 segundos de inactividad:

```yaml
metadata:
  annotations:
    nginx.ingress.kubernetes.io/proxy-read-timeout: "3600"
    nginx.ingress.kubernetes.io/proxy-send-timeout: "3600"
    nginx.ingress.kubernetes.io/websocket-services: "realtime-api-service"
```
