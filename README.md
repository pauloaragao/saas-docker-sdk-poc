# SaaS Docker SDK API - API para gerenciamento de containers Docker

> **Status**: ✅ Em desenvolvimento ativo (MVP funcional) | API operacional com CRUD parcial de containers e documentação Swagger

## 🔍 Visão Geral

### **Objetivo**
Disponibilizar uma API REST para operar containers Docker de forma simples e padronizada, facilitando integração com painéis web, automações e ferramentas internas.

### **Proposta de Valor**
- **Para desenvolvedores backend**: integração rápida com Docker sem escrever código direto no SDK em cada serviço.
- **Para equipes de plataforma/DevOps**: centralização de operações básicas de container via endpoints HTTP.
- **Para produtos internos**: base pronta para construir interfaces com dropdown de containers e ações operacionais.

## 🚀 Funcionalidades Implementadas

### **Gerenciamento de Containers**
- **Listagem de containers** com FastAPI (`GET /api/v1/containers`) com filtro de parados (`all=true`).
- **Detalhamento de container** por ID/nome (`GET /api/v1/containers/{container_id}`).
- **Criação de container por imagem** (`POST /api/v1/containers`) com validação de payload.
- **Exclusão de container em execução** (`DELETE /api/v1/containers/{container_id}`) com regra de negócio para evitar remoção de container parado.
- **Opções para dropdown** (`GET /api/v1/containers/running/options`) retornando `container_name` + `image` em formato amigável para UI.

### **Observabilidade e Saúde**
- **Health check** (`GET /health`) indicando status da API e conectividade com Docker daemon.
- **Swagger/OpenAPI** disponível em `/docs` e `/openapi.json`.

### **Arquitetura e Boas Práticas**
- **Separação por camadas (DDD + SOLID)** com módulos `domain`, `services`, `infrastructure` e `routes`.
- **Injeção de dependência** para desacoplar regras de negócio do acesso ao Docker SDK.
- **Tratamento consistente de exceções** com respostas HTTP padronizadas.

## 🧰 Stack Tecnológica

### **Backend**
- **FastAPI (0.129.0)** - framework web para APIs REST com documentação automática.
- **Uvicorn (0.40.0)** - servidor ASGI para execução da aplicação.
- **Docker SDK for Python (7.1.0)** - integração programática com engine Docker.
- **Pydantic (2.12.5)** - validação e serialização dos modelos de entrada/saída.

### **Frontend**
- **Não aplicável neste repositório** (projeto atual expõe apenas API backend).

## 🗂️ Estrutura do Projeto

```text
saas-docker-sdk-poc/
├── app/
│   ├── domain/
│   │   ├── exceptions.py                # Exceções de domínio
│   │   └── repositories/
│   │       └── docker_repository.py     # Contrato (interface) do repositório
│   ├── infrastructure/
│   │   └── docker_sdk_repository.py     # Implementação concreta via Docker SDK
│   ├── routes/
│   │   ├── items.py                     # Endpoints de containers
│   │   └── users.py                     # Endpoint de health
│   ├── services/
│   │   └── docker_service.py            # Casos de uso/regras de negócio
│   ├── dependencies.py                  # Wiring de dependências
│   └── main.py                          # Entrypoint FastAPI
├── Dockerfile                           # Build da imagem da API
├── docker-compose.yml                   # Orquestração local com hot reload
├── requirements.txt                     # Dependências Python
├── test_api.py                          # Script simples de testes manuais
├── how-start.md                         # Guia rápido de execução
└── README.md
```

## ▶️ Como Executar

### **Pré-requisitos**
- Python **3.11+**
- Docker Engine
- Docker Compose V2 (`docker compose`)

### **Instalação e Execução (Docker - recomendado)**

```bash
docker compose up --build -d
```

Verificar API:

```bash
curl http://localhost:8000/health
```

Documentação interativa:
- Swagger: http://localhost:8000/docs
- OpenAPI JSON: http://localhost:8000/openapi.json

Parar ambiente:

```bash
docker compose down
```

### **Instalação e Execução (local)**

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

## ⚙️ Configuração de Variáveis de Ambiente

| Variável | Descrição | Valor Padrão | Obrigatória |
|----------|-----------|--------------|-------------|
| WATCHFILES_FORCE_POLLING | Força polling de arquivos para hot reload em ambientes com eventos limitados | true (via Compose) | Não |
| PYTHONDONTWRITEBYTECODE | Evita geração de arquivos `.pyc` no container | 1 (Dockerfile) | Não |
| PYTHONUNBUFFERED | Força logs sem buffer para melhor observabilidade em container | 1 (Dockerfile) | Não |

## 📡 Endpoints Principais

### **Containers**
- `GET /api/v1/containers` - lista containers em execução
- `GET /api/v1/containers?all=true` - lista também os parados
- `GET /api/v1/containers/{container_id}` - detalhes do container
- `GET /api/v1/containers/running/options` - opções para dropdown (`container_name`, `image`)
- `POST /api/v1/containers` - cria container por imagem
- `DELETE /api/v1/containers/{container_id}` - remove container em execução

### **Sistema**
- `GET /health` - saúde da API e status de conexão com Docker

## 🧪 Exemplo de Uso Prático

Criar container:

```bash
curl -X POST http://localhost:8000/api/v1/containers \
	-H "Content-Type: application/json" \
	-d '{"image":"nginx:alpine","name":"tmp-nginx-ddd"}'
```

Listar opções para dropdown:

```bash
curl http://localhost:8000/api/v1/containers/running/options
```

Excluir container em execução:

```bash
curl -X DELETE http://localhost:8000/api/v1/containers/tmp-nginx-ddd
```

## 🗺️ Próximos Passos (Roadmap)

### **Fase 1 - Robustez e DX**
- Adicionar testes automatizados para service e rotas (cenários de sucesso/erro).
- Criar modelos de resposta tipados para padronizar contratos da API.
- Melhorar tratamento de erros de pull/autenticação de imagens privadas.

### **Fase 2 - Operações de Containers**
- Implementar start/stop/restart de containers.
- Incluir logs e métricas básicas por container.
- Adicionar paginação e filtros avançados na listagem.

### **Fase 3 - Segurança e Produção**
- Adicionar autenticação/autorização para endpoints sensíveis.
- Definir perfil de execução `dev`/`prod` no Compose.
- Publicar pipeline CI para lint, testes e build de imagem.

