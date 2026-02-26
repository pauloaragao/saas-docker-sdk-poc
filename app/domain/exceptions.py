class DockerUnavailableError(Exception):
    pass


class ContainerNotFoundError(Exception):
    pass


class DockerOperationError(Exception):
    pass


class ContainerNotRunningError(Exception):
    pass
