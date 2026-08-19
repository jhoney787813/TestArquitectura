#!/usr/bin/env bash

echo "=========================================================================="
echo "    PLAYBOOK KUBERNETES - EJERCICIO 3: REAL-TIME ARCHITECTURE"
echo "=========================================================================="
echo ""

echo "[PASO 1] Verificar Pods del Gateway en tiempo real y el generador Kafka"
echo "Comando: kubectl get pods -l 'app in (realtime-api, event-generator)'"
kubectl get pods -l 'app in (realtime-api, event-generator)' || echo " (Ejecutar en clúster activo)"
echo ""

echo "[PASO 2] Inspeccionar conexiones SSE y WebSockets activas en el Pod Gateway"
echo "Comando: kubectl exec -it \$(kubectl get pod -l app=realtime-api -o jsonpath='{.items[0].metadata.name}') -- curl -s http://localhost:8000/health"
echo ""

echo "[PASO 3] Monitorear transmisión de eventos SSE desde el clúster"
echo "Comando: kubectl exec -it \$(kubectl get pod -l app=realtime-api -o jsonpath='{.items[0].metadata.name}') -- curl -N http://localhost:8000/api/v1/realtime/stream"
echo ""
