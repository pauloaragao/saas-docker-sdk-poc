from abc import ABC, abstractmethod
from typing import Any


class DockerRepository(ABC):
    @abstractmethod
    def is_available(self) -> bool:
        raise NotImplementedError

    @abstractmethod
    def list_containers(self, include_stopped: bool = False) -> list[dict[str, Any]]:
        raise NotImplementedError

    @abstractmethod
    def get_container_details(self, container_id: str) -> dict[str, Any]:
        raise NotImplementedError

    @abstractmethod
    def create_container(self, image: str, name: str | None = None) -> dict[str, Any]:
        raise NotImplementedError

    @abstractmethod
    def delete_running_container(self, container_id: str) -> None:
        raise NotImplementedError

    @abstractmethod
    def list_running_container_options(self) -> list[dict[str, str]]:
        raise NotImplementedError
