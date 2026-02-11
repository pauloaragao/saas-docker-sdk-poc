"""
Testes do SDK
"""
import pytest
from sdk.core.client import DockerClient
from docker.errors import DockerException


class TestDockerClient:
    """Testes do DockerClient"""
    
    def test_docker_client_init(self):
        """Testar inicialização do cliente Docker"""
        try:
            client = DockerClient()
            assert client.is_connected()
        except DockerException:
            pytest.skip("Docker não está disponível")
    
    def test_docker_version(self):
        """Testar obtenção da versão do Docker"""
        try:
            client = DockerClient()
            version = client.get_version()
            assert 'Version' in version
        except DockerException:
            pytest.skip("Docker não está disponível")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
