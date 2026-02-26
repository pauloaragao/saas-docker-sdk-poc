from functools import lru_cache

from app.services.docker_service import DockerService
from app.infrastructure.docker_sdk_repository import DockerSdkRepository


@lru_cache
def get_docker_repository() -> DockerSdkRepository:
	return DockerSdkRepository()


def get_docker_service() -> DockerService:
	return DockerService(repository=get_docker_repository())
