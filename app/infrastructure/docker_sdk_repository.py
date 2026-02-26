from typing import Any

import docker
from docker.errors import DockerException, NotFound

from app.domain.exceptions import (
    ContainerNotFoundError,
    ContainerNotRunningError,
    DockerOperationError,
)
from app.domain.repositories.docker_repository import DockerRepository


class DockerSdkRepository(DockerRepository):
    def __init__(self):
        try:
            self._client = docker.from_env()
        except DockerException:
            self._client = None

    def is_available(self) -> bool:
        if self._client is None:
            return False
        try:
            self._client.ping()
            return True
        except DockerException:
            return False

    def list_containers(self, include_stopped: bool = False) -> list[dict[str, Any]]:
        try:
            containers = self._client.containers.list(all=include_stopped)
            return [self._serialize_container(container) for container in containers]
        except DockerException as error:
            raise DockerOperationError(f"Erro ao listar containers: {error}") from error

    def get_container_details(self, container_id: str) -> dict[str, Any]:
        try:
            container = self._client.containers.get(container_id)
            data = self._serialize_container(container)
            data["networks"] = list(container.attrs["NetworkSettings"]["Networks"].keys())
            data["mounts"] = [mount["Source"] for mount in container.attrs["Mounts"]]
            return data
        except NotFound as error:
            raise ContainerNotFoundError(f"Container '{container_id}' não encontrado") from error
        except DockerException as error:
            raise DockerOperationError(f"Erro ao obter detalhes do container: {error}") from error

    def create_container(self, image: str, name: str | None = None) -> dict[str, Any]:
        try:
            container = self._client.containers.run(
                image=image,
                name=name,
                detach=True,
            )
            return self._serialize_container(container)
        except DockerException as error:
            raise DockerOperationError(f"Erro ao criar container: {error}") from error

    def delete_running_container(self, container_id: str) -> None:
        try:
            container = self._client.containers.get(container_id)
            container.reload()
            if container.status != "running":
                raise ContainerNotRunningError(
                    f"Container '{container_id}' não está em execução"
                )
            container.remove(force=True)
        except NotFound as error:
            raise ContainerNotFoundError(f"Container '{container_id}' não encontrado") from error
        except ContainerNotRunningError:
            raise
        except DockerException as error:
            raise DockerOperationError(f"Erro ao excluir container: {error}") from error

    def list_running_container_options(self) -> list[dict[str, str]]:
        try:
            containers = self._client.containers.list(all=False)
            options: list[dict[str, str]] = []
            for container in containers:
                image = (
                    container.image.tags[0]
                    if container.image.tags
                    else container.image.short_id
                )
                options.append(
                    {
                        "value": container.short_id,
                        "label": f"{container.name} ({image})",
                        "container_name": container.name,
                        "image": image,
                    }
                )
            return options
        except DockerException as error:
            raise DockerOperationError(
                f"Erro ao listar opções de containers: {error}"
            ) from error

    @staticmethod
    def _serialize_container(container) -> dict[str, Any]:
        return {
            "id": container.short_id,
            "name": container.name,
            "status": container.status,
            "image": container.image.tags[0] if container.image.tags else container.image.short_id,
            "created": container.attrs["Created"],
            "ports": container.ports,
            "labels": container.labels,
        }
