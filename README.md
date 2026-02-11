# SaaS Docker SDK PoC

SDK completo para gerenciar containers Docker com Python. Inclui API FastAPI, API Flask, CLI Python e biblioteca SDK.

## 🎯 Features

- ✅ **SDK Python** - Biblioteca para build e gerencimento de containers
- ✅ **API FastAPI** - API assíncrona com Swagger
- ✅ **API Flask** - API síncrona para criar/gerenciar containers
- ✅ **CLI** - Interface de linha de comando
- ✅ **Logging com Cores** - Saída formatada
- ✅ **Exemplos** - 4 exemplos práticos de uso

## 📁 Estrutura do Projeto

```
saas-docker-sdk-poc/
├── app/                              # Aplicação FastAPI
│   ├── main.py                       # App FastAPI
│   ├── api/                          # APIs FastAPI
│   │   ├── routes/
│   │   └── schemas/
│   └── sdk_api/                      # 🆕 API Flask para SDK
│       ├── app.py                    # App Flask factory
│       ├── routes.py                 # Endpoints da API
│       └── schemas.py                # Schemas Pydantic
│
├── sdk/                              # 🐳 SDK Docker
│   ├── core/
│   │   └── client.py                 # Cliente Docker
│   ├── builders/
│   │   └── container_builder.py      # Build de imagens
│   ├── managers/
│   │   └── container_manager.py      # Gerenciamento de containers
│   ├── utils/
│   │   ├── logger.py                 # Logging com cores
│   │   └── helpers.py                # Funções auxiliares
│   └── cli.py                        # CLI do SDK
│
├── examples/                         # 📚 Exemplos
│   ├── 01_basic_usage.py
│   ├── 02_build_and_run.py
│   ├── 03_container_management.py
│   └── 04_flask_sdk_api.py           # 🆕 Exemplo Flask API
│
├── config/                           # Configurações
├── tests/                            # Testes
├── Dockerfile                        # Imagem Docker
├── docker-compose.yml                # Orquestração
├── requirements.txt                  # Dependências
├── flask_run.py                      # 🆕 Entry point Flask
├── Makefile                          # Automação
├── SDK.md                            # Documentação SDK
├── FLASK_API.md                      # 🆕 Documentação Flask API
└── README.md                         # Este arquivo
```

## 🚀 Quick Start

### 1. Instalar Dependências
```bash
make install
# ou
pip install -r requirements.txt
```

### 2. Escolha uma opção:

#### Opção A: FastAPI (porta 8000)
```bash
make run
# ou
docker-compose up -d
```

#### Opção B: Flask SDK API (porta 5000)
```bash
make flask-run
# ou
python flask_run.py
```

#### Opção C: SDK Python (via código/CLI)
```bash
# CLI
python -m sdk.cli list --all

# Python
python examples/01_basic_usage.py
```

## 🌐 APIs Disponíveis

### FastAPI (porta 8000) - Recomendado ⭐
- **Swagger Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: `GET /api/v1/health`
- **Containers**: `/api/containers`, `/api/containers/{id}`, etc
- **Imagens**: `/api/images`, etc

### Flask SDK API (porta 5000)  
- **Health**: http://localhost:5000/health
- **Containers**: `/api/containers`, `/api/containers/{id}`, etc
- **Imagens**: `/api/images`, etc

## 📚 Documentação

- [SDK.md](./SDK.md) - Documentação completa SDK Python
- [FLASK_API.md](./FLASK_API.md) - Documentação API Flask
- [ESTRUTURA.md](./ESTRUTURA.md) - Estrutura FastAPI original
- [DOCKER_SDK_STRUCTURE.md](./DOCKER_SDK_STRUCTURE.md) - Arquitetura SDK

## 🐳 Usando a API Flask

### Iniciar
```bash
make flask-run
# A API estará em http://localhost:5000
```

### Exemplos cURL

**Build de imagem:**
```bash
curl -X POST http://localhost:5000/api/images \
  -H "Content-Type: application/json" \
  -d '{
    "dockerfile_path": "./Dockerfile",
    "tag": "myapp:latest",
    "context_path": "."
  }'
```

**Executar container:**
```bash
curl -X POST http://localhost:5000/api/containers \
  -H "Content-Type: application/json" \
  -d '{
    "image": "myapp:latest",
    "name": "myapp-container",
    "ports": {8000: 8000},
    "environment": {"DEBUG": "True"}
  }'
```

**Listar containers:**
```bash
curl http://localhost:5000/api/containers
```

**Obter logs:**
```bash
curl http://localhost:5000/api/containers/myapp-container/logs
```

**Parar container:**
```bash
curl -X POST http://localhost:5000/api/containers/myapp-container/stop
```

**Remover container:**
```bash
curl -X DELETE http://localhost:5000/api/containers/myapp-container?force=true
```

### Testar API Flask
```bash
make flask-test
# ou
python examples/04_flask_sdk_api.py
```

## 🐍 Usando o SDK Python

### Uso Programático

```python
from sdk import DockerClient, ContainerBuilder, ContainerManager

# Conectar ao Docker
client = DockerClient()

# Build de imagem
builder = ContainerBuilder(client)
image_id = builder.build_image(
    dockerfile_path="./Dockerfile",
    tag="myapp:latest"
)

# Executar container
manager = ContainerManager(client)
container_id = manager.run(
    image="myapp:latest",
    name="myapp",
    ports={8000: 8000}
)

# Listar logs
logs = manager.get_logs(container_id)
print(logs)
```

### Via CLI

```bash
# Build
python -m sdk.cli build --dockerfile ./Dockerfile --tag myapp:latest

# Run
python -m sdk.cli run myapp:latest --name myapp -p 8000:8000

# Listar containers
python -m sdk.cli list --all

# Logs
python -m sdk.cli logs myapp --lines 50

# Parar
python -m sdk.cli stop myapp

# Remover
python -m sdk.cli remove myapp --force
```

## 🛠️ Comandos Make

```bash
make help          # Ver todos os comandos

# Docker Compose
make install       # Instalar dependências
make run           # Iniciar containers
make stop          # Parar containers
make clean         # Remover containers e volumes
make logs          # Ver logs

# SDK Python
make sdk-list      # Listar containers via SDK
make sdk-build     # Build via SDK
make sdk-run       # Run via SDK

# Flask API
make flask-run     # Rodar API Flask
make flask-test    # Testar API Flask

# Testes
make test          # Rodar testes Python
```

## 🔧 Configuração

### Variáveis de Ambiente (.env)
