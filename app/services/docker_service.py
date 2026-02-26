from typing import Any

from app.domain.exceptions import DockerUnavailableError
from app.domain.repositories.docker_repository import DockerRepository


class DockerService:
    def __init__(self, repository: DockerRepository):
        self._repository = repository

    def get_health(self) -> dict[str, str]:
        docker_status = "connected" if self._repository.is_available() else "disconnected"
        return {"status": "healthy", "docker": docker_status}

    def list_containers(self, include_stopped: bool = False) -> list[dict[str, Any]]:
        if not self._repository.is_available():
            raise DockerUnavailableError("Docker não está disponível")
        return self._repository.list_containers(include_stopped=include_stopped)

    def get_container_details(self, container_id: str) -> dict[str, Any]:
        if not self._repository.is_available():
            raise DockerUnavailableError("Docker não está disponível")
        return self._repository.get_container_details(container_id=container_id)

    def create_container(self, image: str, name: str | None = None) -> dict[str, Any]:
        if not self._repository.is_available():
            raise DockerUnavailableError("Docker não está disponível")
        return self._repository.create_container(image=image, name=name)

    def delete_running_container(self, container_id: str) -> None:
        if not self._repository.is_available():
            raise DockerUnavailableError("Docker não está disponível")
        self._repository.delete_running_container(container_id=container_id)

    def list_running_container_options(self) -> list[dict[str, str]]:
        if not self._repository.is_available():
            raise DockerUnavailableError("Docker não está disponível")
        return self._repository.list_running_container_options()
