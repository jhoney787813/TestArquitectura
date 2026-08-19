# Guía de Diagnóstico de Seguridad y Revocación en Kubernetes (Ejercicio 4)

## 📌 Diagnóstico del Esquema de Seguridad Multi-Protocolo en K8s

En Kubernetes, la seguridad unificada para REST, SOAP y WebSockets requiere centralizar la revocación de tokens mediante un **Redis Cluster distribuido** y asegurar la propagación del contexto de seguridad en los Ingress Controllers.

---

## 1. Verificar Estado del Servidor de Autenticación y Lista Negra

```bash
# Consultar el conteo de tokens revocados en la Redis Blacklist
kubectl exec -it $(kubectl get pod -l app=security-api -o jsonpath='{.items[0].metadata.name}') -- curl -s http://localhost:8000/health
```

---

## 2. Verificar el WSDL del Servicio SOAP en el Clúster

```bash
# Consultar la definición WSDL del servicio SOAP en el entorno
kubectl exec -it $(kubectl get pod -l app=security-api -o jsonpath='{.items[0].metadata.name}') -- curl -s http://localhost:8000/soap/PolicySoapService.svc?wsdl
```

---

## 3. Configuración de Seguridad en Ingress Controller (TLS & Authorization)

 annotations recomendadas para Ingress:

```yaml
metadata:
  annotations:
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
    nginx.ingress.kubernetes.io/proxy-buffer-size: "16k"
    nginx.ingress.kubernetes.io/enable-cors: "true"
```
