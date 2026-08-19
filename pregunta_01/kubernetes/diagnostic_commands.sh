#!/usr/bin/env bash

# Script ejecutable de diagnóstico en Kubernetes para Ejercicio 1
# Diagnóstico de Latencia P95 = 8s con CPU 10% y RAM 30%

echo "=========================================================================="
echo "    PLAYBOOK DE DIAGNÓSTICO EN KUBERNETES - EJERCICIO 1 (SENIOR ARCHITECT)"
echo "=========================================================================="
echo ""

NAMESPACE="${1:-default}"
APP_LABEL="app=api-rest-service"

echo "[PASO 1] Verificar el consumo de recursos de los Pods (CPU / Memoria)"
echo "Comando: kubectl top pods -n $NAMESPACE -l $APP_LABEL"
kubectl top pods -n "$NAMESPACE" -l "$APP_LABEL" || echo " (Ejecutar en clúster activo)"
echo ""

echo "[PASO 2] Inspeccionar eventos del clúster y estado de los Pods"
echo "Comando: kubectl get pods -n $NAMESPACE -l $APP_LABEL -o wide"
kubectl get pods -n "$NAMESPACE" -l "$APP_LABEL" -o wide || echo " (Ejecutar en clúster activo)"
echo ""

echo "[PASO 3] Analizar logs en tiempo real para descartar errores fatales o OOMKilled"
echo "Comando: kubectl logs -n $NAMESPACE -l $APP_LABEL --tail=100"
kubectl logs -n "$NAMESPACE" -l "$APP_LABEL" --tail=50 || echo " (Ejecutar en clúster activo)"
echo ""

echo "[PASO 4] Verificar estado de sockets TCP y concurrencia dentro de un Pod activo"
echo "Comando: kubectl exec -it \$(kubectl get pod -n $NAMESPACE -l $APP_LABEL -o jsonpath='{.items[0].metadata.name}') -- netstat -tan | grep 8080"
POD_NAME=$(kubectl get pod -n "$NAMESPACE" -l "$APP_LABEL" -o jsonpath='{.items[0].metadata.name}' 2>/dev/null)
if [ -n "$POD_NAME" ]; then
    kubectl exec -it "$POD_NAME" -n "$NAMESPACE" -- netstat -tan 2>/dev/null || echo " (No se pudo ejecutar netstat dentro del Pod)"
fi
echo ""

echo "[PASO 5] Consultar métricas de Ingress Controller (Latencia HTTP NGINX/Istio)"
echo "Comando: kubectl logs -n ingress-nginx -l app.kubernetes.io/name=ingress-nginx --tail=50 | grep '$APP_LABEL'"
echo ""

echo "[PASO 6] Consultar métricas de Prometheus mediante PromQL en la terminal (curl Prometheus API)"
echo "Consultar latencia P95:"
echo '  curl -g -s "http://prometheus.monitoring:9090/api/v1/query?query=histogram_quantile(0.95,sum(rate(http_request_duration_seconds_bucket[5m]))by(le))"'
echo "Consultar CPU:"
echo '  curl -g -s "http://prometheus.monitoring:9090/api/v1/query?query=sum(rate(container_cpu_usage_seconds_total{pod=~\"api-rest.*\"}[5m]))/sum(kube_pod_container_resource_limits{pod=~\"api-rest.*\",resource=\"cpu\"})*100"'
echo ""

echo "=========================================================================="
echo " RESUMEN DIAGNÓSTICO: CPU/RAM bajas + Latencia Alta = I/O WAIT / POOL EXHAUSTION"
echo "=========================================================================="
