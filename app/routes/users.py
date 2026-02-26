from fastapi import APIRouter, Depends

from app.application.services.docker_service import DockerService
from app.dependencies import get_docker_service

router = APIRouter(tags=["health"])


@router.get("/health")
def health_check(service: DockerService = Depends(get_docker_service)):
	return service.get_health()
