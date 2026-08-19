#!/usr/bin/env bash

echo "=========================================================================="
echo "    PLAYBOOK KUBERNETES - EJERCICIO 4: AUTHENTICATION & AUTHORIZATION"
echo "=========================================================================="
echo ""

echo "[PASO 1] Verificar Pods de la API de Seguridad Multi-Protocolo"
echo "Comando: kubectl get pods -l app=security-api"
kubectl get pods -l app=security-api || echo " (Ejecutar en clúster activo)"
echo ""

echo "[PASO 2] Auditar las llaves revocadas en Redis Blacklist desde un Pod"
echo "Comando: kubectl exec -it \$(kubectl get pod -l app=security-api -o jsonpath='{.items[0].metadata.name}') -- curl -s http://localhost:8000/health"
echo ""

echo "[PASO 3] Probar validación de WSDL SOAP desde el clúster"
echo "Comando: kubectl exec -it \$(kubectl get pod -l app=security-api -o jsonpath='{.items[0].metadata.name}') -- curl -s http://localhost:8000/soap/PolicySoapService.svc?wsdl"
echo ""
