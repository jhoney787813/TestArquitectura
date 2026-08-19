#!/usr/bin/env bash

echo "=========================================================================="
echo "    PLAYBOOK KUBERNETES - EJERCICIO 5: OBSERVABILITY & DIAGNOSTICS"
echo "=========================================================================="
echo ""

echo "[PASO 1] Verificar Pods de la API de Observabilidad"
echo "Comando: kubectl get pods -l app=observability-api"
kubectl get pods -l app=observability-api || echo " (Ejecutar en clúster activo)"
echo ""

echo "[PASO 2] Auditar Métricas de Prometheus expuestas en /metrics"
echo "Comando: kubectl exec -it \$(kubectl get pod -l app=observability-api -o jsonpath='{.items[0].metadata.name}') -- curl -s http://localhost:8000/metrics"
echo ""

echo "[PASO 3] Probar generación de ProblemDetails RFC 7807 (422 Unprocessable Entity)"
echo "Comando: kubectl exec -it \$(kubectl get pod -l app=observability-api -o jsonpath='{.items[0].metadata.name}') -- curl -i -s http://localhost:8000/api/v1/good-practice/policies/rule-error"
echo ""
