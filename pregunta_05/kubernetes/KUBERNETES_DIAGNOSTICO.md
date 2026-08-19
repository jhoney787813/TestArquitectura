# Guía de Diagnóstico de Observabilidad en Kubernetes (Ejercicio 5)

## 📌 Configuración de Auto-Scraping y Tracing en K8s

En Kubernetes, la observabilidad enterprise requiere que las aplicaciones utilicen el **OpenTelemetry Operator** para inyectar automáticamente cabeceras `traceparent` en el ingress y anotaciones de **Prometheus Scraping**.

---

## 1. Anotaciones de Pod para Scraping Automático de Prometheus

En `deployment.yaml`:

```yaml
template:
  metadata:
    annotations:
      prometheus.io/scrape: "true"
      prometheus.io/port: "8000"
      prometheus.io/path: "/metrics"
```

---

## 2. Verificar Métricas de Prometheus desde la Consola del Clúster

```bash
kubectl exec -it $(kubectl get pod -l app=observability-api -o jsonpath='{.items[0].metadata.name}') -- curl -s http://localhost:8000/metrics
```

---

## 3. Verificar Formato RFC 7807 (ProblemDetails JSON) y Header W3C TraceContext

```bash
kubectl exec -it $(kubectl get pod -l app=observability-api -o jsonpath='{.items[0].metadata.name}') -- curl -i -s http://localhost:8000/api/v1/good-practice/policies/rule-error
```
