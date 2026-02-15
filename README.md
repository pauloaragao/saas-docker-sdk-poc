# SaaS Docker SDK API

Uma API completa para gerenciamento de containers Docker com interface Swagger integrada.

## 🚀 Funcionalidades

- ✅ **Interface Swagger** - Documentação interativa da API
- ✅ **Gerenciamento de Containers** - Criar, iniciar, parar, remover containers
- ✅ **Gerenciamento de Imagens** - Construir, listar, remover imagens Docker
- ✅ **Health Checks** - Monitoramento de saúde da aplicação e dependências
- ✅ **Redis Cache** - Sistema de cache para otimização
- ✅ **Docker Compose** - Orquestração completa de serviços

## 📋 Pré-requisitos

- Docker
- Docker Compose
- Python 3.11+ (para desenvolvimento local)

## 🛠️ Instalação e Execução

### 1. Clone o repositório
```bash
git clone <repository-url>
cd saas-docker-sdk-poc
```

### 2. Configure as variáveis de ambiente
```bash
cp .env.example .env
```

### 3. Execute com Docker Compose
```bash
docker-compose up --build
```

### 4. Acesse a aplicação

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/api/v1/health

## 📡 Endpoints Principais

### Health Checks
- `GET /api/v1/health` - Status geral da aplicação
- `GET /api/v1/health/ready` - Verificação de prontidão
- `GET /api/v1/health/live` - Verificação de disponibilidade

### Containers
- `GET /api/v1/docker/containers` - Listar containers
- `POST /api/v1/docker/containers` - Criar container
- `POST /api/v1/docker/containers/{id}/start` - Iniciar container
- `POST /api/v1/docker/containers/{id}/stop` - Parar container
- `DELETE /api/v1/docker/containers/{id}` - Remover container

### Imagens Docker
- `GET /api/v1/docker/images` - Listar imagens
- `POST /api/v1/docker/images/build` - Construir imagem
- `DELETE /api/v1/docker/images/{id}` - Remover imagem

### Sistema Docker
- `GET /api/v1/docker/info` - Informações do sistema Docker

## 🏗️ Estrutura do Projeto

```
saas-docker-sdk-poc/
├── app/
│   ├── __init__.py
│   ├── main.py                 # Aplicação FastAPI principal
│   ├── core/
│   │   ├── __init__.py
│   │   └── config.py          # Configurações da aplicação
│   └── api/
│       ├── __init__.py
│       └── routes/
│           ├── __init__.py
│           ├── health.py      # Endpoints de health check
│           └── docker.py      # Endpoints Docker
├── logs/                      # Pasta para logs
├── Dockerfile                 # Configuração da imagem
├── docker-compose.yml        # Orquestração dos serviços
├── requirements.txt          # Dependências Python
├── .env.example             # Exemplo de variáveis de ambiente
└── README.md               # Este arquivo
```

## 🔧 Desenvolvimento Local

### 1. Criar ambiente virtual
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\\Scripts\\activate  # Windows
```

### 2. Instalar dependências
```bash
pip install -r requirements.txt
```

### 3. Executar aplicação
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

## 🐳 Comandos Docker Úteis

### Parar serviços
```bash
docker-compose down
```

### Reconstruir imagens
```bash
docker-compose up --build --force-recreate
```

### Ver logs
```bash
docker-compose logs -f api
```

### Acessar container
```bash
docker-compose exec api bash
```

## 📊 Monitoramento

A aplicação inclui health checks abrangentes que monitoram:

- **Sistema**: CPU, memória e disco
- **Docker**: Conectividade e versão
- **Redis**: Conectividade e disponibilidade

## 🔐 Segurança

- CORS configurado adequadamente
- Usuário não-privilegiado no container
- Health checks para monitoramento
- Variáveis de ambiente para configuração sensível

## 🚀 Produção

Para ambiente de produção, atualize:

1. Variáveis no `.env`:
   ```bash
   ENV=production
   SECRET_KEY=sua-chave-secreta-segura
   ```

2. Configure CORS adequadamente:
   ```python
   ALLOWED_HOSTS = ["https://seu-dominio.com"]
   ```

3. Use HTTPS e proxy reverso (Nginx/Traefik)

## 📝 Logs

Os logs são salvos em:
- Container: `/app/logs/`
- Host: `./logs/`

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT.

## 🆘 Suporte

Para suporte, abra uma issue no repositório ou entre em contato com a equipe de desenvolvimento.