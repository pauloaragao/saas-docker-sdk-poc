# Como iniciar o projeto

## Opção 1 (recomendada): Docker Compose

Pré-requisitos:
- Docker instalado e em execução
- Docker Compose V2 (`docker compose`)

### 1) Subir a API

```bash
docker compose up --build -d
```

### 2) Validar se está no ar

```bash
curl http://localhost:8000/health
```

Resposta esperada:

```json
{"status":"healthy","docker":"connected"}
```

### 3) Acessar documentação

- Swagger: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### 4) Ver logs

```bash
docker compose logs -f api
```

### 5) Parar tudo

```bash
docker compose down
```

---

## Opção 2: Rodar local (sem Compose)

### 1) Ativar virtualenv

```bash
source .venv/bin/activate
```

### 2) Instalar dependências

```bash
pip install -r requirements.txt
```

### 3) Subir API

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### 4) Testar endpoint

```bash
curl http://localhost:8000/health
```

---

## Troubleshooting rápido

- `docker compose: command not found`:
  - Atualize Docker para versão com Compose V2.
- Porta `8000` em uso:
  - Pare o processo atual ou altere o mapeamento de porta em `docker-compose.yml`.
- `docker":"disconnected` no `/health`:
  - Verifique se o Docker daemon está ativo e se o socket `/var/run/docker.sock` existe no host.