#!/usr/bin/env bash

echo "=========================================================================="
echo "    PLAYBOOK KUBERNETES - EJERCICIO 7: CQRS & MEDIATOR (.NET 9)"
echo "=========================================================================="
echo ""

echo "[PASO 1] Verificar Pods de la API CQRS"
echo "Comando: kubectl get pods -l app=cqrs-mediator-api"
kubectl get pods -l app=cqrs-mediator-api || echo " (Ejecutar en clúster activo)"
echo ""

echo "[PASO 2] Probar ejecución de CreatePolicyCommand (Escritura via MediatR)"
echo "Comando: kubectl exec -it \$(kubectl get pod -l app=cqrs-mediator-api -o jsonpath='{.items[0].metadata.name}') -- curl -s -X POST http://localhost:8000/api/v1/commands/policies/create -H 'Content-Type: application/json' -d '{\"policy_type\":\"VIDA\",\"insured_name\":\"K8s User\",\"insured_email\":\"k8s@seguros.com\",\"amount\":5000}'"
echo ""

echo "[PASO 3] Probar ejecución de GetPolicyByIdQuery (Lectura ultra-rápida Read Model)"
echo "Comando: kubectl exec -it \$(kubectl get pod -l app=cqrs-mediator-api -o jsonpath='{.items[0].metadata.name}') -- curl -s http://localhost:8000/api/v1/queries/policies"
echo ""
