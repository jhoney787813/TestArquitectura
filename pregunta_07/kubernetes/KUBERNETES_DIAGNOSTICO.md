# Guía de Diagnóstico de la Arquitectura CQRS y Mediator en Kubernetes (Ejercicio 7)

## 📌 Principios de Diagnóstico de CQRS en Kubernetes

En un entorno Kubernetes empresarial, la separación CQRS permite escalar de forma independiente las réplicas de los microservicios de **Lectura (Queries)** y **Escritura (Commands)**.

---

## 1. Verificación de Salud del Pod CQRS

```bash
kubectl get pods -l app=cqrs-mediator-api
```

---

## 2. Diagnóstico de Ejecución de Comandos (Write Model)

```bash
kubectl exec -it $(kubectl get pod -l app=cqrs-mediator-api -o jsonpath='{.items[0].metadata.name}') -- curl -i -X POST http://localhost:8000/api/v1/commands/policies/create -H "Content-Type: application/json" -d '{"policy_type":"AUTO","insured_name":"Jhon K8s","insured_email":"jhon@seguros.com","amount":3500}'
```

---

## 3. Diagnóstico de Consultas Hiper-rápidas (Read Model / Proyecciones DTO)

```bash
kubectl exec -it $(kubectl get pod -l app=cqrs-mediator-api -o jsonpath='{.items[0].metadata.name}') -- curl -s http://localhost:8000/api/v1/queries/policies
```
