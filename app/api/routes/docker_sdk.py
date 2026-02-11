"""
Docker SDK Routes - Endpoints para gerenciar containers via SDK
"""
import logging
from typing import Optional, List
from fastapi import APIRouter, HTTPException, Query, Body
from pydantic import BaseModel

from sdk import DockerClient, ContainerBuilder, ContainerManager

logger = logging.getLogger(__name__)

router = APIRouter()

# Modelos Pydantic
class BuildImageRequest(BaseModel):
    """Request para build de imagem"""
    dockerfile_path: str
    tag: str
    context_path: Optional[str] = None
    build_args: Optional[dict] = None


class RunContainerRequest(BaseModel):
    """Request para executar container"""
    image: str
    name: Optional[str] = None
    ports: Optional[dict] = None
    environment: Optional[dict] = None
    volumes: Optional[dict] = None
    detach: bool = True


class ContainerActionRequest(BaseModel):
    """Request para ações em container"""
    container_id: str


class SuccessResponse(BaseModel):
    """Response de sucesso"""
    success: bool = True
    message: str
    data: Optional[dict] = None


class ErrorResponse(BaseModel):
    """Response de erro"""
    error: str
    message: str
    details: Optional[dict] = None


# Inicializar clientes Docker
docker_client: Optional[DockerClient] = None
container_builder: Optional[ContainerBuilder] = None
container_manager: Optional[ContainerManager] = None


def init_docker_clients():
    """Inicializar clientes Docker (lazy loading)"""
    global docker_client, container_builder, container_manager
    
    if docker_client is None:
        try:
            docker_client = DockerClient()
            container_builder = ContainerBuilder(docker_client)
            container_manager = ContainerManager(docker_client)
            logger.info("✓ Docker clients initialized")
        except Exception as e:
            logger.error(f"✗ Error initializing Docker clients: {str(e)}")
            raise


# ============================================================================
# CONTAINERS ENDPOINTS
# ============================================================================

@router.get("/containers", tags=["containers"], summary="Listar containers")
async def list_containers(all: bool = Query(False, description="Incluir containers parados")):
    """
    Listar todos os containers
    
    - **all**: Incluir status parados (default: False)
    
    Returns:
    - Lista de containers com info de nome, ID, status, etc
    """
    try:
        init_docker_clients()
        containers = container_manager.list_containers(all=all)
        
        return {
            "success": True,
            "message": f"{len(containers)} container(s) encontrado(s)",
            "data": {
                "count": len(containers),
                "containers": containers
            }
        }
    
    except Exception as e:
        logger.error(f"Error listing containers: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao listar containers: {str(e)}"
        )


@router.get("/containers/{container_id}", tags=["containers"], summary="Obter info do container")
async def get_container(container_id: str):
    """
    Obter informações detalhadas de um container
    
    - **container_id**: ID ou nome do container
    
    Returns:
    - Objeto com informações do container (status, portas, etc)
    """
    try:
        init_docker_clients()
        container = container_manager.get_container(container_id)
        
        if not container:
            raise HTTPException(
                status_code=404,
                detail=f"Container '{container_id}' não encontrado"
            )
        
        return {
            "success": True,
            "message": f"Informações do container '{container_id}'",
            "data": container
        }
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting container: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/containers", tags=["containers"], summary="Executar novo container")
async def run_container(request: RunContainerRequest):
    """
    Executar um novo container
    
    Body:
    - **image**: Nome ou ID da imagem
    - **name**: Nome do container (opcional)
    - **ports**: Mapeamento de portas (ex: {"8000": "8000"})
    - **environment**: Variáveis de ambiente (ex: {"DEBUG": "True"})
    - **volumes**: Volumes (ex: {"/host/path": "/container/path"})
    - **detach**: Executar em background (default: True)
    
    Returns:
    - Container ID
    """
    try:
        init_docker_clients()
        
        container_id = container_manager.run(
            image=request.image,
            name=request.name,
            ports=request.ports,
            environment=request.environment,
            volumes=request.volumes,
            detach=request.detach,
        )
        
        logger.info(f"✓ Container executado: {container_id[:12]}")
        
        return {
            "success": True,
            "message": f"Container executado com sucesso",
            "data": {
                "container_id": container_id,
                "name": request.name,
                "image": request.image
            }
        }
    
    except Exception as e:
        logger.error(f"Error running container: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/containers/{container_id}/start", tags=["containers"], summary="Iniciar container")
async def start_container(container_id: str):
    """Iniciar um container parado"""
    try:
        init_docker_clients()
        container_manager.start(container_id)
        
        return {
            "success": True,
            "message": f"Container '{container_id}' iniciado",
            "data": {"container_id": container_id}
        }
    
    except Exception as e:
        logger.error(f"Error starting container: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/containers/{container_id}/stop", tags=["containers"], summary="Parar container")
async def stop_container(container_id: str, timeout: int = Query(10, ge=0)):
    """Parar um container em execução"""
    try:
        init_docker_clients()
        container_manager.stop(container_id, timeout=timeout)
        
        return {
            "success": True,
            "message": f"Container '{container_id}' parado",
            "data": {"container_id": container_id}
        }
    
    except Exception as e:
        logger.error(f"Error stopping container: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/containers/{container_id}", tags=["containers"], summary="Remover container")
async def remove_container(container_id: str, force: bool = Query(False), volumes: bool = Query(False)):
    """Remover um container"""
    try:
        init_docker_clients()
        container_manager.remove(container_id, force=force, v=volumes)
        
        return {
            "success": True,
            "message": f"Container '{container_id}' removido",
            "data": {"container_id": container_id}
        }
    
    except Exception as e:
        logger.error(f"Error removing container: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/containers/{container_id}/logs", tags=["containers"], summary="Obter logs")
async def get_container_logs(container_id: str, lines: int = Query(100, ge=1)):
    """Obter logs de um container"""
    try:
        init_docker_clients()
        logs = container_manager.get_logs(container_id, lines=lines)
        
        return {
            "success": True,
            "message": f"Logs do container '{container_id}'",
            "data": {
                "container_id": container_id,
                "lines": lines,
                "logs": logs
            }
        }
    
    except Exception as e:
        logger.error(f"Error getting logs: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# IMAGES ENDPOINTS
# ============================================================================

@router.get("/images", tags=["images"], summary="Listar imagens")
async def list_images():
    """
    Listar todas as imagens Docker disponíveis
    
    Returns:
    - Lista de imagens com tags e tamanho
    """
    try:
        init_docker_clients()
        images = container_builder.list_images()
        
        return {
            "success": True,
            "message": f"{len(images)} imagem(ns) encontrada(s)",
            "data": {
                "count": len(images),
                "images": images
            }
        }
    
    except Exception as e:
        logger.error(f"Error listing images: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/images", tags=["images"], summary="Build de imagem")
async def build_image(request: BuildImageRequest):
    """
    Construir uma nova imagem Docker
    
    Body:
    - **dockerfile_path**: Caminho para o Dockerfile
    - **tag**: Tag da imagem (ex: 'myapp:latest')
    - **context_path**: Diretório raiz do build (opcional)
    - **build_args**: Argumentos de build (opcional)
    
    Returns:
    - ID da imagem construída
    """
    try:
        init_docker_clients()
        
        image_id = container_builder.build_image(
            dockerfile_path=request.dockerfile_path,
            tag=request.tag,
            context_path=request.context_path,
            build_args=request.build_args,
        )
        
        logger.info(f"✓ Imagem construída: {image_id[:12]}")
        
        return {
            "success": True,
            "message": f"Imagem '{request.tag}' construída com sucesso",
            "data": {
                "image_id": image_id,
                "tag": request.tag
            }
        }
    
    except Exception as e:
        logger.error(f"Error building image: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/images/{image_id}", tags=["images"], summary="Remover imagem")
async def remove_image(image_id: str, force: bool = Query(False)):
    """Remover uma imagem Docker"""
    try:
        init_docker_clients()
        container_builder.remove_image(image_id, force=force)
        
        return {
            "success": True,
            "message": f"Imagem '{image_id}' removida",
            "data": {"image_id": image_id}
        }
    
    except Exception as e:
        logger.error(f"Error removing image: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
