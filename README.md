# SaaS Docker SDK PoC

API de exemplo construída com FastAPI e Docker.

## Estrutura do Projeto

```
saas-docker-sdk-poc/
├── app/                          # Aplicação principal
│   ├── __init__.py
│   ├── main.py                  # Entry point da aplicação
│   └── api/                     # APIs da aplicação
│       ├── routes/              # Rotas da API
│       │   ├── __init__.py
│       │   └── health.py       # Health check routes
│       └── schemas/             # Pydantic schemas/models
│           └── __init__.py
│
├── config/                       # Configurações
│   ├── __init__.py
│   └── settings.py              # Settings da aplicação
│
├── tests/                        # Testes
│   ├── __init__.py
│   └── unit/                    # Unit tests
│       └── __init__.py
│
├── Dockerfile                    # Configuração Docker
├── docker-compose.yml           # Orquestração de containers
├── requirements.txt             # Dependências Python
├── .dockerignore                # Arquivos ignorados no build Docker
├── .env.example                 # Exemplo de variáveis de ambiente
└── README.md                    # Este arquivo
```

## Pré-requisitos

- Docker >= 20.10
- Docker Compose >= 2.0

## Instalação

### 1. Clonar o repositório

```bash
git clone <repository-url>
cd saas-docker-sdk-poc
```

### 2. Configurar variáveis de ambiente

```bash
cp .env.example .env
```

## Execução

### Com Docker Compose (Recomendado)

```bash
# Iniciar os containers
docker-compose up -d

# Parar os containers
docker-compose down

# Visualizar logs
docker-compose logs -f api
```

### Sem Docker

```bash
# Criar ambiente virtual
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate

# Instalar dependências
pip install -r requirements.txt

# Executar aplicação
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Documentação da API

Após iniciar a aplicação, ela estará disponível em `http://localhost:8000`

### Swagger UI (Documentação Interativa)
- URL: `http://localhost:8000/docs`
- Permite testar os endpoints diretamente
- Exibe schemas de request/response
- Suporte a autenticação

### ReDoc (Documentação Alternativa)
- URL: `http://localhost:8000/redoc`
- Documentação em formato limpo
- Melhor para leitura em mobile

### OpenAPI Schema
- URL: `http://localhost:8000/openapi.json`
- Arquivo JSON com toda a especificação OpenAPI 3.0

## Endpoints

## Testes

```bash
# Executar testes
pytest

# Com coverage
pytest --cov=app tests/
```

## Desenvolvimento

### Adicionar novas rotas

1. Criar arquivo em `app/api/routes/`
2. Importar o router em `app/main.py`
3. Adicionar com `app.include_router()`

### Adicionar novos schemas

1. Criar modelos Pydantic em `app/api/schemas/`
2. Usar nos request/response models das rotas

### Variáveis de ambiente

Configurar in `.env`:
- `ENVIRONMENT` - Ambiente (development/production)
- `DEBUG` - Mode debug
- `HOST` - Host da aplicação
- `PORT` - Porta da aplicação
- `REDIS_URL` - URL do Redis

## Build para produção

```bash
# Build da imagem Docker
docker build -t saas-api:latest .

# Executar container
docker run -p 8000:8000 saas-api:latest
```

## Estrutura de Camadas

```
requests
  ↓
routes (app/api/routes/)
  ↓
schemas (app/api/schemas/)
  ↓
config (config/)
  ↓
responses
```

## Licença

MIT
