import os
import time
import json
import uuid
import random
from typing import Dict, Optional
from datetime import datetime
from fastapi import FastAPI, Request, Response, HTTPException, status, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel

app = FastAPI(
    title="Observability & Exception Handling API - Ejercicio 5 (OpenTelemetry, Prometheus & RFC 7807)",
    description="Demostración del diagnóstico de catch(Exception ex) { return BadRequest(); } y solución técnica con OpenTelemetry, Modelo de Richardson y RFC 7807.",
    version="5.0.0"
)

# Métricas Prometheus en memoria
prometheus_metrics = {
    "http_requests_total": 0,
    "http_errors_total": 0,
    "exceptions_by_type": {},
    "requests_by_status": {"200": 0, "400": 0, "404": 0, "409": 0, "422": 0, "500": 0, "503": 0}
}

# Colores ANSI para logs visuales en consola
COLOR_CYAN = "\033[96m"
COLOR_YELLOW = "\033[93m"
COLOR_GREEN = "\033[92m"
COLOR_RED = "\033[91m"
COLOR_MAGENTA = "\033[95m"
COLOR_BOLD = "\033[1m"
COLOR_RESET = "\033[0m"


# ==============================================================================
# 🏛️ 1. EXCEPCIONES DOMINIO Y MAPEO A MODELO DE MADUREZ DE RICHARDSON
# ==============================================================================
class DomainException(Exception):
    """Precondición de negocio no cumplida (HTTP 422 Unprocessable Entity)"""
    def __init__(self, message: str, code: str = "DOMAIN_RULE_VIOLATION"):
        self.message = message
        self.code = code
        self.http_status = 422

class ResourceNotFoundException(Exception):
    """Recurso no encontrado en el sistema (HTTP 404 Not Found)"""
    def __init__(self, resource_name: str, resource_id: str):
        self.message = f"El recurso '{resource_name}' con ID '{resource_id}' no existe."
        self.code = "RESOURCE_NOT_FOUND"
        self.http_status = 404

class ConflictException(Exception):
    """Conflicto de estado o duplicidad (HTTP 409 Conflict)"""
    def __init__(self, message: str):
        self.message = message
        self.code = "RESOURCE_CONFLICT"
        self.http_status = 409

class DownstreamDependencyException(Exception):
    """Falla técnica de servicio downstream o base de datos (HTTP 503 Service Unavailable)"""
    def __init__(self, service_name: str, detail: str):
        self.message = f"El servicio externo '{service_name}' no está disponible o respondió con timeout."
        self.code = "DOWNSTREAM_DEPENDENCY_FAILURE"
        self.http_status = 503


# ==============================================================================
# 📡 2. MIDDLEWARE GLOBAL DE OBSERVABILIDAD, OPENTELEMETRY TRACING & PROBLEM DETAILS
# ==============================================================================
@app.middleware("http")
async def observability_middleware(request: Request, call_next):
    start_time = time.time()
    
    # 🔍 Generar o propagar TraceId y SpanId (Estándar W3C traceparent)
    incoming_traceparent = request.headers.get("traceparent")
    if incoming_traceparent and len(incoming_traceparent.split("-")) >= 3:
        parts = incoming_traceparent.split("-")
        trace_id = parts[1]
        span_id = str(uuid.uuid4())[:16]
    else:
        trace_id = uuid.uuid4().hex
        span_id = uuid.uuid4().hex[:16]

    w3c_traceparent = f"00-{trace_id}-{span_id}-01"
    request.state.trace_id = trace_id
    request.state.span_id = span_id
    request.state.traceparent = w3c_traceparent

    prometheus_metrics["http_requests_total"] += 1

    try:
        response: Response = await call_next(request)
        elapsed_ms = round((time.time() - start_time) * 1000, 2)
        
        # Inyectar cabeceras W3C TraceContext en la respuesta
        response.headers["traceparent"] = w3c_traceparent
        response.headers["X-Trace-ID"] = trace_id
        
        status_code_str = str(response.status_code)
        prometheus_metrics["requests_by_status"][status_code_str] = prometheus_metrics["requests_by_status"].get(status_code_str, 0) + 1

        now_str = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        log_json = {
            "timestamp": now_str,
            "level": "INFO" if response.status_code < 400 else "WARN",
            "trace_id": trace_id,
            "span_id": span_id,
            "method": request.method,
            "path": request.url.path,
            "status_code": response.status_code,
            "duration_ms": elapsed_ms
        }
        print(f"{COLOR_CYAN}[OPENTELEMETRY LOG] {json.dumps(log_json)}{COLOR_RESET}", flush=True)
        return response

    except Exception as ex:
        elapsed_ms = round((time.time() - start_time) * 1000, 2)
        prometheus_metrics["http_errors_total"] += 1
        
        # Mapeo Semántico según Modelo de Madurez de Richardson & RFC 7807 ProblemDetails
        if isinstance(ex, DomainException):
            status_code = ex.http_status
            title = "Domain Rule Violation"
            error_code = ex.code
            detail = ex.message
        elif isinstance(ex, ResourceNotFoundException):
            status_code = ex.http_status
            title = "Resource Not Found"
            error_code = ex.code
            detail = ex.message
        elif isinstance(ex, ConflictException):
            status_code = ex.http_status
            title = "Conflict Error"
            error_code = ex.code
            detail = ex.message
        elif isinstance(ex, DownstreamDependencyException):
            status_code = ex.http_status
            title = "Service Unavailable"
            error_code = ex.code
            detail = ex.message
        else:
            status_code = 500
            title = "Internal Server Error"
            error_code = "UNHANDLED_EXCEPTION"
            detail = "Ocurrió una falla interna en el servidor. Consulte con la traza de observabilidad."

        status_code_str = str(status_code)
        prometheus_metrics["requests_by_status"][status_code_str] = prometheus_metrics["requests_by_status"].get(status_code_str, 0) + 1
        prometheus_metrics["exceptions_by_type"][error_code] = prometheus_metrics["exceptions_by_type"].get(error_code, 0) + 1

        now_str = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        
        # Log Estructurado en JSON (Formato Serilog / Loki)
        log_json = {
            "timestamp": now_str,
            "level": "ERROR",
            "trace_id": trace_id,
            "span_id": span_id,
            "method": request.method,
            "path": request.url.path,
            "status_code": status_code,
            "error_code": error_code,
            "exception_type": type(ex).__name__,
            "message": str(ex),
            "duration_ms": elapsed_ms
        }
        print(f"{COLOR_RED}[SERILOG / LOKI STRUCTURED ERROR LOG] {json.dumps(log_json)}{COLOR_RESET}", flush=True)

        # 📄 RESPUESTA ESTÁNDAR RFC 7807 (ProblemDetails JSON)
        problem_details = {
            "type": f"https://api.seguros.com/errors/{error_code.lower()}",
            "title": title,
            "status": status_code,
            "detail": detail,
            "code": error_code,
            "instance": request.url.path,
            "trace_id": trace_id,
            "timestamp": datetime.utcnow().isoformat()
        }

        return JSONResponse(
            status_code=status_code,
            content=problem_details,
            headers={
                "Content-Type": "application/problem+json",
                "traceparent": w3c_traceparent,
                "X-Trace-ID": trace_id
            }
        )


# ==============================================================================
# 🌐 ENDPOINTS DE PRUEBA Y DEMOSTRACIÓN DE ANTIPATRÓN vs BUENAS PRÁCTICAS
# ==============================================================================
@app.get("/health")
async def health():
    return {
        "status": "UP",
        "observability_stack": ["OpenTelemetry", "Prometheus", "Serilog", "Jaeger", "RFC7807"],
        "metrics_summary": prometheus_metrics
    }

# 🔴 ANTIPATRÓN: Demostración de catch(Exception ex) { return BadRequest(); }
@app.get("/api/v1/bad-practice/policies/{policy_id}")
async def bad_practice_policy(policy_id: str):
    """
    DEMOSTRACIÓN DEL ANTIPATRÓN EVALUADO:
    catch(Exception ex) { return BadRequest(); }
    Responde un 400 BadRequest genérico o 500 ocultando la causa real y destruyendo las trazas.
    """
    try:
        if policy_id == "not-found":
            raise ResourceNotFoundException("Póliza", policy_id)
        elif policy_id == "db-error":
            raise DownstreamDependencyException("SQL Database Server", "Connection Timeout (Error 50001)")
        elif policy_id == "rule-error":
            raise DomainException("La póliza ya caducó y no se puede modificar.")
        else:
            raise Exception("NullReferenceException fatal no capturada en objeto de inspección")
    except Exception as ex:
        # ❌ ANTIPATRÓN: Captura la excepción genérica y retorna BadRequest() ciego sin trazas ni código semántico
        return JSONResponse(
            status_code=400,
            content={
                "message": "BadRequest genérico: Ocurrió un error sin traza ni detalle semántico de Richardson."
            }
        )

# 🟢 BUENA PRÁCTICA: Mapeo semántico de Richardson + OpenTelemetry Tracing
@app.get("/api/v1/good-practice/policies/{policy_id}")
async def good_practice_policy(policy_id: str, request: Request):
    """
    SOLUCIÓN TÉCNICA DE OBSERVABILIDAD:
    Las excepciones de Dominio e Infraestructura se elevan al Middleware Global,
    el cual asigna el código HTTP semántico correcto (Richardson Level 2),
    mantiene el TraceId de OpenTelemetry y responde en formato RFC 7807 ProblemDetails.
    """
    if policy_id == "not-found":
        raise ResourceNotFoundException("Póliza", policy_id)
    elif policy_id == "db-error":
        raise DownstreamDependencyException("SQL Database Cluster", "Timeout de 5000ms al consultar réplica de lectura.")
    elif policy_id == "rule-error":
        raise DomainException("La póliza de vehículo se encuentra cancelada por mora en el pago.")
    elif policy_id == "conflict":
        raise ConflictException("La emisión de la póliza ya fue registrada por otra transacción concurrente.")
    elif policy_id == "unhandled":
        raise RuntimeError("Falla crítica en memoria RAM o puntero nulo en cálculo actuarial")

    return {
        "status": "SUCCESS",
        "policy_id": policy_id,
        "insured": "Jhon (Arquitecto)",
        "coverage": "$500,000 USD",
        "trace_id": request.state.trace_id
    }

# 📊 ENDPOINT PROMETHEUS METRICS (/metrics)
@app.get("/metrics")
async def get_prometheus_metrics():
    """
    Exportador de métricas en formato texto de Prometheus.
    """
    metrics_text = f"""# HELP http_requests_total Total number of HTTP requests processed.
# TYPE http_requests_total counter
http_requests_total {prometheus_metrics['http_requests_total']}

# HELP http_errors_total Total number of HTTP errors encountered.
# TYPE http_errors_total counter
http_errors_total {prometheus_metrics['http_errors_total']}

# HELP requests_by_status HTTP requests grouped by status code.
# TYPE requests_by_status counter
"""
    for code, count in prometheus_metrics["requests_by_status"].items():
        metrics_text += f'requests_by_status{{code="{code}"}} {count}\n'

    for err_code, count in prometheus_metrics["exceptions_by_type"].items():
        metrics_text += f'exceptions_by_type{{error_code="{err_code}"}} {count}\n'

    return Response(content=metrics_text, media_type="text/plain")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
