#!/usr/bin/env bash

echo "=========================================================================="
echo "    PLAYBOOK KUBERNETES - EJERCICIO 2: RESILIENCIA EN EMISIÓN DE PÓLIZAS"
echo "=========================================================================="
echo ""

echo "[PASO 1] Verificar Pods de la API y los Workers asíncronos"
echo "Comando: kubectl get pods -l 'app in (policy-api, notification-worker)'"
kubectl get pods -l 'app in (policy-api, notification-worker)' || echo " (Ejecutar en clúster activo)"
echo ""

echo "[PASO 2] Inspeccionar logs del Worker para verificar consumo de Outbox y retries"
echo "Comando: kubectl logs -l app=notification-worker --tail=50 -f"
echo ""

echo "[PASO 3] Consultar estado de la Dead Letter Queue (DLQ) mediante curl en Pod"
echo "Comando: kubectl exec -it \$(kubectl get pod -l app=notification-worker -o jsonpath='{.items[0].metadata.name}') -- curl -s http://localhost:8090/api/v1/dlq"
echo ""

echo "[PASO 4] Verificar estado del Circuit Breaker de SMS"
echo "Comando: kubectl exec -it \$(kubectl get pod -l app=mock-gateways -o jsonpath='{.items[0].metadata.name}') -- curl -s http://localhost:8091/health"
echo ""
