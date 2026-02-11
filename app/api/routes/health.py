"""
Health check routes
"""
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


class HealthResponse(BaseModel):
    """Health check response model"""
    status: str
    message: str = "API is healthy and running"


@router.get(
    "/health",
    response_model=HealthResponse,
    summary="Health Check",
    description="Verifica se a API está rodando e saudável"
)
async def health_check() -> HealthResponse:
    """
    Health check endpoint
    
    Retorna o status da aplicação.
    
    **Returns:**
    - `status`: Status atual da API (ok)
    - `message`: Mensagem descritiva
    """
    return HealthResponse(status="ok")
