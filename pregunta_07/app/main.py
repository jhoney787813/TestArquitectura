import os
import time
import json
import uuid
from typing import Dict, List, Any, Optional
from datetime import datetime
from fastapi import FastAPI, Request, Response, HTTPException, status, Query, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

app = FastAPI(
    title="CQRS & Mediator Pattern API - Ejercicio 7 (.NET 9 Clean Architecture)",
    description="Implementación del Patrón CQRS (Command Query Responsibility Segregation) y Mediator (MediatR Pipeline Behaviors) en .NET 9.",
    version="7.0.0"
)

# Base de Datos Simulada para la Separación CQRS
# Write Model: Modelo de Dominio rico con validaciones ACID
write_db: Dict[str, Dict[str, Any]] = {}

# Read Model: Proyecciones denormalizadas optimizadas para lectura ultra-rápida (Read Replica / Redis Cache)
read_model_db: Dict[str, Dict[str, Any]] = {}

# Colores ANSI para logs visuales en consola
COLOR_CYAN = "\033[96m"
COLOR_YELLOW = "\033[93m"
COLOR_GREEN = "\033[92m"
COLOR_RED = "\033[91m"
COLOR_MAGENTA = "\033[95m"
COLOR_BOLD = "\033[1m"
COLOR_RESET = "\033[0m"


# ==============================================================================
# 🏛️ 1. DTOs DE COMMANDS Y QUERIES (.NET 9 CQRS Messages)
# ==============================================================================
class CreatePolicyCommand(BaseModel):
    policy_type: str = Field(..., example="VIDA") # "VIDA", "AUTO", "HOGAR"
    insured_name: str = Field(..., example="Jhon E. Arquitecto")
    insured_email: str = Field(..., example="jhoney7878@gmail.com")
    amount: float = Field(..., gt=0, example=150000.0)

class EmitPolicyCommand(BaseModel):
    policy_id: str
    payment_reference: str

class GetPolicyByIdQuery(BaseModel):
    policy_id: str

class GetPoliciesSummaryQuery(BaseModel):
    policy_type: Optional[str] = None


# ==============================================================================
# 🔀 2. PATRÓN MEDIATOR & PIPELINE BEHAVIORS (.NET 9 MediatR Bus Simulation)
# ==============================================================================
class MediatorBus:
    """
    Simulación del Bus Orquestador MediatR en .NET 9.
    Enruta Commands y Queries a sus respectivos Handlers pasando por los Pipeline Behaviors.
    """
    @staticmethod
    async def send(message: Any, request: Request) -> Any:
        start_time = time.time()
        trace_id = getattr(request.state, "trace_id", uuid.uuid4().hex)
        now_str = datetime.now().strftime("%H:%M:%S.%f")[:-3]

        # ----------------------------------------------------------------------
        # PIPELINE BEHAVIOR 1: ValidationBehavior (FluentValidation)
        # ----------------------------------------------------------------------
        if isinstance(message, CreatePolicyCommand):
            if message.amount <= 0:
                raise HTTPException(status_code=422, detail="VALIDATION_FAILED: El monto debe ser mayor a cero.")
            if "@" not in message.insured_email:
                raise HTTPException(status_code=422, detail="VALIDATION_FAILED: Formato de correo electrónico inválido.")

        # ----------------------------------------------------------------------
        # ENRUTAMIENTO A HANDLERS (Command Handlers vs Query Handlers)
        # ----------------------------------------------------------------------
        print(f"{COLOR_CYAN}[{now_str}] 🔀 [MEDIATR BUS] Despachando {type(message).__name__} (TraceId: {trace_id[:8]}){COLOR_RESET}", flush=True)

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

        # ----------------------------------------------------------------------
        # PIPELINE BEHAVIOR 2: LoggingAndPerformanceBehavior
        # ----------------------------------------------------------------------
        elapsed_ms = round((time.time() - start_time) * 1000, 2)
        print(f"{COLOR_GREEN}[{now_str}] ✅ [MEDIATR SUCCESS] {type(message).__name__} procesado en {elapsed_ms} ms{COLOR_RESET}", flush=True)
        
        return result


# ==============================================================================
# ✍️ 3. COMMAND HANDLERS (Pila de Escritura - Write Model)
# ==============================================================================
class CommandHandlers:
    @staticmethod
    async def handle_create_policy(command: CreatePolicyCommand, trace_id: str) -> Dict[str, Any]:
        policy_id = f"POL-NET9-{str(uuid.uuid4())[:8].upper()}"
        now_iso = datetime.utcnow().isoformat()

        # 1. Escritura en el Write Model (Entidad de Dominio ACID)
        policy_entity = {
            "policy_id": policy_id,
            "policy_type": command.policy_type.upper(),
            "insured_name": command.insured_name,
            "insured_email": command.insured_email,
            "amount": command.amount,
            "status": "DRAFT",
            "created_at": now_iso,
            "version": 1
        }
        write_db[policy_id] = policy_entity

        # 2. Publicación de Evento de Dominio & Actualización de la Proyección (Read Model)
        # Sincronización asíncrona (Eventual Consistency)
        read_model_db[policy_id] = {
            "id": policy_id,
            "display_title": f"Póliza de {command.policy_type.upper()} - {command.insured_name}",
            "status": "DRAFT",
            "insured": command.insured_name,
            "amount_formatted": f"${command.amount:,.2f} USD",
            "updated_at": now_iso
        }

        print(f"{COLOR_YELLOW} ✍️ [WRITE STACK] Command {policy_id} creado en Write DB y proyectado a Read Model.{COLOR_RESET}", flush=True)

        return {
            "status": "CREATED",
            "policy_id": policy_id,
            "message": "Comando ejecutado exitosamente mediante MediatR Pipeline Behavior.",
            "trace_id": trace_id
        }

    @staticmethod
    async def handle_emit_policy(command: EmitPolicyCommand, trace_id: str) -> Dict[str, Any]:
        if command.policy_id not in write_db:
            raise HTTPException(status_code=404, detail=f"Póliza '{command.policy_id}' no encontrada en la base de datos de escritura.")

        entity = write_db[command.policy_id]
        entity["status"] = "ACTIVE"
        entity["version"] += 1
        entity["payment_ref"] = command.payment_reference

        # Sincronizar actualización en Read Model
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
# 📖 4. QUERY HANDLERS (Pila de Lectura - Read Model)
# ==============================================================================
class QueryHandlers:
    @staticmethod
    async def handle_get_policy_by_id(query: GetPolicyByIdQuery, trace_id: str) -> Dict[str, Any]:
        # Lectura ultra-rápida directamente del Read Model (Bypasea la lógica de dominio)
        if query.policy_id not in read_model_db:
            raise HTTPException(status_code=404, detail=f"La póliza '{query.policy_id}' no existe en el modelo de lectura.")

        projection = read_model_db[query.policy_id]
        print(f"{COLOR_MAGENTA} 📖 [READ STACK] Query ejecutada directamente sobre Read Model (Respuesta en < 2ms).{COLOR_RESET}", flush=True)

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
# 🌐 5. ENDPOINTS DE PRESENTACIÓN (CQRS Controllers)
# ==============================================================================
@app.middleware("http")
async def trace_middleware(request: Request, call_next):
    request.state.trace_id = uuid.uuid4().hex
    response = await call_next(request)
    response.headers["X-Trace-ID"] = request.state.trace_id
    return response

@app.get("/health")
async def health():
    return {
        "status": "UP",
        "cqrs_architecture": "CQRS + MediatR Pipeline Behavior (.NET 9)",
        "write_db_count": len(write_db),
        "read_model_count": len(read_model_db)
    }

# ✍️ COMMAND ENDPOINTS (Escritura via Mediator Bus)
@app.post("/api/v1/commands/policies/create", status_code=201)
async def create_policy_endpoint(command: CreatePolicyCommand, request: Request):
    return await MediatorBus.send(command, request)

@app.post("/api/v1/commands/policies/emit")
async def emit_policy_endpoint(command: EmitPolicyCommand, request: Request):
    return await MediatorBus.send(command, request)

# 📖 QUERY ENDPOINTS (Lectura via Mediator Bus)
@app.get("/api/v1/queries/policies/{policy_id}")
async def get_policy_query_endpoint(policy_id: str, request: Request):
    query = GetPolicyByIdQuery(policy_id=policy_id)
    return await MediatorBus.send(query, request)

@app.get("/api/v1/queries/policies")
async def get_policies_summary_query_endpoint(policy_type: Optional[str] = None, request: Request = None):
    query = GetPoliciesSummaryQuery(policy_type=policy_type)
    return await MediatorBus.send(query, request)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
