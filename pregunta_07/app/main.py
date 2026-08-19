import os
import time
import json
import uuid
from typing import Dict, List, Any, Optional
from datetime import datetime
from fastapi import FastAPI, Request, Response, HTTPException, status, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

app = FastAPI(
    title="CQRS & Mediator Pattern API - Ejercicio 7 (.NET 9 Clean Architecture)",
    description="API ejecutable de la arquitectura C# .NET 9 CQRS con MediatR Pipeline Behaviors, Command Handlers y Query Handlers.",
    version="9.0.0"
)

# Base de Datos Simulada en Memoria (Separación de Escritura y Lectura)
write_db: Dict[str, Dict[str, Any]] = {}
read_model_db: Dict[str, Dict[str, Any]] = {}

# Colores ANSI para logs visuales en consola
COLOR_CYAN = "\033[96m"
COLOR_YELLOW = "\033[93m"
COLOR_GREEN = "\033[92m"
COLOR_RED = "\033[91m"
COLOR_MAGENTA = "\033[95m"
COLOR_RESET = "\033[0m"


# ==============================================================================
# 🏛️ 1. DTOs DE COMMANDS Y QUERIES (Equivalentes a C# .NET 9 MediatR Records)
# ==============================================================================
class CreatePolicyCommand(BaseModel):
    policy_type: str = Field(..., example="VIDA")
    insured_name: str = Field(..., example="Jhon E. Arquitecto Senior")
    insured_email: str = Field(..., example="jhoney7878@gmail.com")
    amount: float = Field(..., gt=0, example=15000.0)

class EmitPolicyCommand(BaseModel):
    policy_id: str
    payment_reference: str

class GetPolicyByIdQuery(BaseModel):
    policy_id: str

class GetPoliciesSummaryQuery(BaseModel):
    policy_type: Optional[str] = None


# ==============================================================================
# 🔀 2. BUS MEDIATR Y PIPELINE BEHAVIORS (C# .NET 9 IPipelineBehavior)
# ==============================================================================
class MediatorBus:
    """
    Despachador In-Memory equivalente a IMediator en .NET 9.
    Enruta mensajes a CommandHandlers y QueryHandlers atravesando los Pipeline Behaviors.
    """
    @staticmethod
    async def send(message: Any, request: Request) -> Any:
        start_time = time.time()
        trace_id = getattr(request.state, "trace_id", uuid.uuid4().hex[:8])
        now_str = datetime.now().strftime("%H:%M:%S.%f")[:-3]

        # ----------------------------------------------------------------------
        # PIPELINE BEHAVIOR 1: ValidationBehavior (FluentValidation)
        # ----------------------------------------------------------------------
        if isinstance(message, CreatePolicyCommand):
            errors = {}
            if message.amount <= 0:
                errors["Amount"] = ["El monto de la póliza debe ser estrictamente mayor a 0."]
            if "@" not in message.insured_email:
                errors["InsuredEmail"] = ["El correo electrónico no tiene un formato válido."]
            if message.policy_type.upper() not in ["VIDA", "AUTO", "HOGAR", "SALUD"]:
                errors["PolicyType"] = ["Tipo de póliza inválido. Permitidos: VIDA, AUTO, HOGAR, SALUD."]
            
            if errors:
                print(f"{COLOR_RED}[{now_str}] ❌ [VALIDATION BEHAVIOR] Falla de validación en CreatePolicyCommand: {errors}{COLOR_RESET}", flush=True)
                return JSONResponse(
                    status_code=422,
                    content={
                        "type": "https://api.seguros.com/errors/validation_failed",
                        "title": "Falla de Validacion en Pipeline Behavior",
                        "status": 422,
                        "detail": "Ocurrieron una o más fallas de validación en la canalización MediatR de .NET 9.",
                        "errors": errors,
                        "trace_id": trace_id
                    }
                )

        # ----------------------------------------------------------------------
        # PIPELINE BEHAVIOR 2: LoggingAndPerformanceBehavior
        # ----------------------------------------------------------------------
        print(f"{COLOR_CYAN}[{now_str}] 🔀 [MEDIATR BUS] Despachando {type(message).__name__} en .NET 9 (TraceId: {trace_id}){COLOR_RESET}", flush=True)

        if isinstance(message, CreatePolicyCommand):
            result = await CommandHandlers.handle_create_policy(message, trace_id)
        elif isinstance(message, EmitPolicyCommand):
            result = await CommandHandlers.handle_emit_policy(message, trace_id)
        elif isinstance(message, GetPolicyByIdQuery):
            result = await QueryHandlers.handle_get_policy_by_id(message, trace_id)
        elif isinstance(message, GetPoliciesSummaryQuery):
            result = await QueryHandlers.handle_get_policies_summary(message, trace_id)
        else:
            raise HTTPException(status_code=400, detail="UNKNOWN_MESSAGE_TYPE")

        elapsed_ms = round((time.time() - start_time) * 1000, 2)
        print(f"{COLOR_GREEN}[{now_str}] ✅ [MEDIATR SUCCESS] {type(message).__name__} procesado exitosamente en {elapsed_ms} ms{COLOR_RESET}", flush=True)
        
        return result


# ==============================================================================
# ✍️ 3. COMMAND HANDLERS (Pila de Escritura / Modelo de Dominio ACID)
# ==============================================================================
class CommandHandlers:
    @staticmethod
    async def handle_create_policy(command: CreatePolicyCommand, trace_id: str) -> Dict[str, Any]:
        policy_id = f"POL-NET9-{str(uuid.uuid4())[:8].upper()}"
        now_iso = datetime.utcnow().isoformat()

        # 1. Escritura en Master Write DB (Modelo Normalizado ACID)
        policy_entity = {
            "policy_id": policy_id,
            "policy_type": command.policy_type.upper(),
            "insured_name": command.insured_name,
            "insured_email": command.insured_email,
            "amount": command.amount,
            "status": "DRAFT",
            "created_at": now_iso,
            "updated_at": now_iso
        }
        write_db[policy_id] = policy_entity

        # 2. Actualización de Proyección en Read Model (Redis / Read Replica)
        read_model_db[policy_id] = {
            "id": policy_id,
            "display_title": f"Póliza de {command.policy_type.upper()} - {command.insured_name}",
            "status": "DRAFT",
            "insured": command.insured_name,
            "amount_formatted": f"${command.amount:,.2f} USD",
            "payment_ref": None,
            "updated_at": now_iso
        }

        print(f"{COLOR_YELLOW} ✍️ [WRITE STACK] Command {policy_id} guardado en Master Write DB y proyectado a Read Model.{COLOR_RESET}", flush=True)

        return {
            "status": "CREATED",
            "policy_id": policy_id,
            "message": "Comando procesado en .NET 9 MediatR Handler.",
            "trace_id": trace_id
        }

    @staticmethod
    async def handle_emit_policy(command: EmitPolicyCommand, trace_id: str) -> Dict[str, Any]:
        if command.policy_id not in write_db:
            return JSONResponse(
                status_code=404,
                content={
                    "type": "https://api.seguros.com/errors/resource_not_found",
                    "title": "Recurso no encontrado",
                    "status": 404,
                    "detail": f"La póliza '{command.policy_id}' no existe en la base de datos de escritura."
                }
            )

        entity = write_db[command.policy_id]
        entity["status"] = "ACTIVE"
        entity["payment_ref"] = command.payment_reference
        entity["updated_at"] = datetime.utcnow().isoformat()

        # Actualizar proyección en Read Model
        read_model_db[command.policy_id]["status"] = "ACTIVE"
        read_model_db[command.policy_id]["payment_ref"] = command.payment_reference
        read_model_db[command.policy_id]["updated_at"] = datetime.utcnow().isoformat()

        print(f"{COLOR_YELLOW} ✍️ [WRITE STACK] Póliza {command.policy_id} emitida y actualizada a estado ACTIVE.{COLOR_RESET}", flush=True)

        return {
            "status": "EMITTED",
            "policy_id": command.policy_id,
            "current_status": "ACTIVE",
            "trace_id": trace_id
        }


# ==============================================================================
# 📖 4. QUERY HANDLERS (Pila de Lectura / Proyecciones DTO < 2ms)
# ==============================================================================
class QueryHandlers:
    @staticmethod
    async def handle_get_policy_by_id(query: GetPolicyByIdQuery, trace_id: str) -> Dict[str, Any]:
        if query.policy_id not in read_model_db:
            return JSONResponse(
                status_code=404,
                content={
                    "type": "https://api.seguros.com/errors/resource_not_found",
                    "title": "Recurso no encontrado",
                    "status": 404,
                    "detail": f"La póliza '{query.policy_id}' no existe en el modelo de lectura."
                }
            )

        projection = read_model_db[query.policy_id]
        print(f"{COLOR_MAGENTA} 📖 [READ STACK] Query ejecutada directamente sobre el Read Model (Respuesta < 2ms).{COLOR_RESET}", flush=True)

        return {
            "status": "SUCCESS",
            "source": "READ_MODEL_PROJECTION",
            "data": projection,
            "trace_id": trace_id
        }

    @staticmethod
    async def handle_get_policies_summary(query: GetPoliciesSummaryQuery, trace_id: str) -> Dict[str, Any]:
        results = list(read_model_db.values())
        if query.policy_type:
            results = [p for p in results if query.policy_type.upper() in p["display_title"]]

        return {
            "status": "SUCCESS",
            "source": "READ_MODEL_PROJECTION",
            "count": len(results),
            "data": results,
            "trace_id": trace_id
        }


# ==============================================================================
# 🌐 5. ENDPOINTS ASP.NET CORE 9.0 POLICIES CONTROLLER
# ==============================================================================
@app.middleware("http")
async def trace_middleware(request: Request, call_next):
    request.state.trace_id = uuid.uuid4().hex[:8]
    response = await call_next(request)
    response.headers["X-Trace-ID"] = request.state.trace_id
    return response

@app.get("/health")
async def health():
    return {
        "status": "UP",
        "framework": ".NET 9.0 (ASP.NET Core Web API)",
        "architecture": "CQRS + MediatR 12.0 Pipeline Behaviors",
        "write_db_records": len(write_db),
        "read_db_records": len(read_model_db)
    }

# ✍️ COMMAND STACK ENDPOINTS (ASP.NET Core 9.0 [HttpPost])
@app.post("/api/v1/policies/commands/create", status_code=201)
async def create_policy_endpoint(command: CreatePolicyCommand, request: Request):
    return await MediatorBus.send(command, request)

@app.post("/api/v1/policies/commands/emit")
async def emit_policy_endpoint(command: EmitPolicyCommand, request: Request):
    return await MediatorBus.send(command, request)

# 📖 QUERY STACK ENDPOINTS (ASP.NET Core 9.0 [HttpGet])
@app.get("/api/v1/policies/queries/{policy_id}")
async def get_policy_query_endpoint(policy_id: str, request: Request):
    query = GetPolicyByIdQuery(policy_id=policy_id)
    return await MediatorBus.send(query, request)

@app.get("/api/v1/policies/queries")
async def get_policies_summary_query_endpoint(policy_type: Optional[str] = None, request: Request = None):
    query = GetPoliciesSummaryQuery(policy_type=policy_type)
    return await MediatorBus.send(query, request)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
