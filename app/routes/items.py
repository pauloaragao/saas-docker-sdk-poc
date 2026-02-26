from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from app.services.docker_service import DockerService
from app.dependencies import get_docker_service
from app.domain.exceptions import (
	ContainerNotFoundError,
	ContainerNotRunningError,
	DockerOperationError,
	DockerUnavailableError,
)

router = APIRouter(prefix="/api/v1/containers", tags=["containers"])


class CreateContainerRequest(BaseModel):
	image: str
	name: str | None = None


@router.get("", response_model=list[dict[str, Any]])
def list_containers(
	all: bool = False,
	service: DockerService = Depends(get_docker_service),
):
	try:
		return service.list_containers(include_stopped=all)
	except DockerUnavailableError as error:
		raise HTTPException(status_code=503, detail=str(error)) from error
	except DockerOperationError as error:
		raise HTTPException(status_code=500, detail=str(error)) from error


@router.get("/{container_id}")
def get_container_details(
	container_id: str,
	service: DockerService = Depends(get_docker_service),
):
	try:
		return service.get_container_details(container_id=container_id)
	except DockerUnavailableError as error:
		raise HTTPException(status_code=503, detail=str(error)) from error
	except ContainerNotFoundError as error:
		raise HTTPException(status_code=404, detail=str(error)) from error
	except DockerOperationError as error:
		raise HTTPException(status_code=500, detail=str(error)) from error


@router.get("/running/options", response_model=list[dict[str, str]])
def list_running_container_options(
	service: DockerService = Depends(get_docker_service),
):
	try:
		return service.list_running_container_options()
	except DockerUnavailableError as error:
		raise HTTPException(status_code=503, detail=str(error)) from error
	except DockerOperationError as error:
		raise HTTPException(status_code=500, detail=str(error)) from error


@router.post("", response_model=dict[str, Any], status_code=201)
def create_container(
	payload: CreateContainerRequest,
	service: DockerService = Depends(get_docker_service),
):
	try:
		return service.create_container(image=payload.image, name=payload.name)
	except DockerUnavailableError as error:
		raise HTTPException(status_code=503, detail=str(error)) from error
	except DockerOperationError as error:
		raise HTTPException(status_code=500, detail=str(error)) from error


@router.delete("/{container_id}", status_code=204)
def delete_running_container(
	container_id: str,
	service: DockerService = Depends(get_docker_service),
):
	try:
		service.delete_running_container(container_id=container_id)
	except DockerUnavailableError as error:
		raise HTTPException(status_code=503, detail=str(error)) from error
	except ContainerNotFoundError as error:
		raise HTTPException(status_code=404, detail=str(error)) from error
	except ContainerNotRunningError as error:
		raise HTTPException(status_code=400, detail=str(error)) from error
	except DockerOperationError as error:
		raise HTTPException(status_code=500, detail=str(error)) from error
