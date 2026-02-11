# 🐳 SaaS Docker SDK

SDK para construir e gerenciar containers Docker localmente com Python.

## 📦 Características

- ✅ **Build de Imagens**: Construir imagens Docker a partir de Dockerfiles
- ✅ **Gerenciamento de Containers**: Criar, executar, parar e remover containers
- ✅ **Logs em Tempo Real**: Acessar logs dos containers
- ✅ **Executar Comandos**: Rodar comandos dentro de containers
- ✅ **CLI Integrada**: Interface de linha de comando para facilitar o uso
- ✅ **Logging com Cores**: Saída formatada e colorida
- ✅ **Type Hints**: Código com suporte a type checking

## 🚀 Instalação

### Pré-requisitos

- Python 3.11+
- Docker instalado e rodando

### Instalar dependências

```bash
pip install -r requirements.txt
```

## 📖 Uso

### 1. Uso Programático (Python)

#### Exemplo Básico

```python
from sdk import DockerClient, ContainerBuilder, ContainerManager
from sdk.utils.logger import setup_logging

# Configurar logging
setup_logging(level="INFO")

# Inicializar cliente Docker
docker_client = DockerClient()

# Criar builder
builder = ContainerBuilder(docker_client)

# Build da imagem
image_id = builder.build_image(
    dockerfile_path="./Dockerfile",
    tag="myapp:latest",
    context_path="."
)

# Criar manager
manager = ContainerManager(docker_client)

# Executar container
container_id = manager.run(
    image="myapp:latest",
    name="myapp-container",
    ports={8000: 8000},
    detach=True
)

# Verificar status
containers = manager.list_containers()
for container in containers:
    print(f"{container['name']} - {container['status']}")
```

#### Build de Imagem

```python
builder = ContainerBuilder(docker_client)

# Build simples
image_id = builder.build_image(
    dockerfile_path="./Dockerfile",
    tag="myapp:1.0",
    context_path="."
)

# Build com argumentos
image_id = builder.build_image(
    dockerfile_path="./Dockerfile",
    tag="myapp:prod",
    context_path=".",
    build_args={
        "environment": "production",
        "version": "1.0.0"
    }
)

# Build do Git
image_id = builder.build_from_git(
    git_url="https://github.com/user/repo.git",
    tag="myapp:latest"
)
```

#### Executar Container

```python
manager = ContainerManager(docker_client)

# Run simples
container_id = manager.run(
    image="myapp:latest",
    name="myapp",
    detach=True
)

# Run com portas e variáveis de ambiente
container_id = manager.run(
    image="myapp:latest",
    name="myapp",
    ports={8000: 8000, 5432: 5432},
    environment={
        "DEBUG": "True",
        "DATABASE_URL": "postgresql://localhost:5432/mydb"
    },
    volumes={
        "/host/path": "/container/path"
    },
    detach=True
)
```

#### Gerenciar Containers

```python
manager = ContainerManager(docker_client)

# Listar containers
containers = manager.list_containers(all=True)

# Obter informações
info = manager.get_container("myapp")

# Parar container
manager.stop("myapp")

# Iniciar container
manager.start("myapp")

# Remover container
manager.remove("myapp", force=True, volumes=True)

# Obter logs
logs = manager.get_logs("myapp", lines=100)
print(logs)

# Executar comando
output = manager.execute_command("myapp", "pip list")
print(output)
```

### 2. Uso via CLI

```bash
# Build de imagem
python -m sdk.cli build --dockerfile ./Dockerfile --tag myapp:latest --context .

# Executar container
python -m sdk.cli run myapp:latest --name myapp -p 8000:8000 -e DEBUG=True

# Listar containers
python -m sdk.cli list --all

# Ver logs
python -m sdk.cli logs myapp --lines 50

# Parar container
python -m sdk.cli stop myapp

# Iniciar container
python -m sdk.cli start myapp

# Remover container
python -m sdk.cli remove myapp --force --volumes
```

## 📚 Exemplos

Veja a pasta `examples/` para exemplos mais completos:

- `01_basic_usage.py` - Uso básico (conectar, listar)
- `02_build_and_run.py` - Build e execução de container
- `03_container_management.py` - Gerenciamento de containers

```bash
# Executar exemplos
python examples/01_basic_usage.py
python examples/02_build_and_run.py
python examples/03_container_management.py
```

## 🏗️ Arquitetura

```
sdk/
├── core/                      # Núcleo do SDK
│   └── client.py             # Cliente Docker principal
├── builders/                  # Builders
│   └── container_builder.py  # Build de imagens
├── managers/                  # Managers
│   └── container_manager.py  # Gerenciamento de containers
├── utils/                     # Utilitários
│   ├── logger.py             # Logging com cores
│   └── helpers.py            # Funções auxiliares
├── cli.py                     # Interface CLI
└── __init__.py               # Exports principais
```

## 📋 API Reference

### DockerClient

```python
DockerClient(base_url: Optional[str] = None)
├── get_version() -> dict
├── get_info() -> dict
└── is_connected() -> bool
```

### ContainerBuilder

```python
ContainerBuilder(docker_client: DockerClient)
├── build_image(dockerfile_path, tag, ...) -> str
├── build_from_git(git_url, tag, ...) -> str
├── list_images() -> List[Dict]
└── remove_image(image_tag, force=False) -> bool
```

### ContainerManager

```python
ContainerManager(docker_client: DockerClient)
├── run(image, name, ports, ...) -> str
├── list_containers(all=False) -> List[Dict]
├── get_container(container_id) -> Dict
├── start(container_id) -> bool
├── stop(container_id, timeout=10) -> bool
├── remove(container_id, force=False, volumes=False) -> bool
├── get_logs(container_id, lines=100) -> str
└── execute_command(container_id, command) -> str
```

## 🔍 Troubleshooting

### "Connection refused" ao conectar Docker

Certifique-se de que:
- Docker está instalado e rodando
- Você tem permissão para acessar o socket Docker
- No Linux, execute: `sudo usermod -aG docker $USER`

### Container não inicia

- Verifique os logs: `manager.get_logs(container_id)`
- Verifique se a imagem existe: `builder.list_images()`
- Verifique as variáveis de ambiente

### Build falha

- Verifique o caminho do Dockerfile
- Verifique permissões de arquivo
- Verifique logs de build

## 📝 Licença

MIT

## 🤝 Contribuindo

1. Fork o projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

## 📞 Suporte

Para reportar bugs ou sugerir features, abra uma issue no repositório.
