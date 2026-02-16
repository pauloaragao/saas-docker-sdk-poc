from fastapi import FastAPI, HTTPException
from typing import List, Dict, Any
import docker
from docker.errors import DockerException

app = FastAPI(
    title="SaaS Docker SDK API",
    description="API para gerenciamento de containers Docker",
    version="1.0.0"
)

# Cliente Docker
try:
    docker_client = docker.from_env()
except DockerException as e:
    print(f"Erro ao conectar ao Docker: {e}")
    docker_client = None

@app.get("/")
def read_root():
    return {
        "message": "SaaS Docker SDK API",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/api/v1/containers", response_model=List[Dict[str, Any]])
def list_containers(all: bool = False):
    """
    Lista todos os containers Docker
    
    - **all**: Se True, lista todos os containers (incluindo parados). Se False, apenas os em execução.
    """
    if docker_client is None:
        raise HTTPException(status_code=503, detail="Docker não está disponível")
    
    try:
        containers = docker_client.containers.list(all=all)
        
        containers_data = []
        for container in containers:
            containers_data.append({
                "id": container.short_id,
                "name": container.name,
                "status": container.status,
                "image": container.image.tags[0] if container.image.tags else container.image.short_id,
                "created": container.attrs['Created'],
                "ports": container.ports,
                "labels": container.labels
            })
        
        return containers_data
    
    except DockerException as e:
        raise HTTPException(status_code=500, detail=f"Erro ao listar containers: {str(e)}")

@app.get("/api/v1/containers/{container_id}")
def get_container_details(container_id: str):
    """
    Obtém detalhes de um container específico
    
    - **container_id**: ID ou nome do container
    """
    if docker_client is None:
        raise HTTPException(status_code=503, detail="Docker não está disponível")
    
    try:
        container = docker_client.containers.get(container_id)
        
        return {
            "id": container.short_id,
            "name": container.name,
            "status": container.status,
            "image": container.image.tags[0] if container.image.tags else container.image.short_id,
            "created": container.attrs['Created'],
            "ports": container.ports,
            "labels": container.labels,
            "networks": list(container.attrs['NetworkSettings']['Networks'].keys()),
            "mounts": [mount['Source'] for mount in container.attrs['Mounts']]
        }
    
    except docker.errors.NotFound:
        raise HTTPException(status_code=404, detail=f"Container '{container_id}' não encontrado")
    except DockerException as e:
        raise HTTPException(status_code=500, detail=f"Erro ao obter detalhes do container: {str(e)}")

@app.get("/health")
def health_check():
    """Verifica a saúde da API e conexão com Docker"""
    docker_status = "connected" if docker_client is not None else "disconnected"
    
    return {
        "status": "healthy",
        "docker": docker_status
    }
