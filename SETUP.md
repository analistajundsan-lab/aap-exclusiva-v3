# Setup Local — AAP Exclusiva v3.0

## Pré-requisitos
- Python 3.12+
- Docker & Docker Compose
- Git

## Instalação (5 minutos)

### 1. Clone do repositório
```bash
git clone https://github.com/[org]/aap-exclusiva-v3.git
cd aap-exclusiva-v3
```

### 2. Setup Python
```bash
python3.12 -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

### 3. Instalar dependências
```bash
pip install -r backend/requirements.txt
```

### 4. Setup .env
```bash
cp .env.example .env
```

### 5. Docker services (PostgreSQL + Redis)
```bash
docker-compose up -d
```

### 6. Run FastAPI
```bash
cd backend
uvicorn main:app --reload --port 8000
```

Acesso: http://localhost:8000/docs (Swagger UI)

### 7. Testes
```bash
pytest tests/ -v --cov=backend
```

## Troubleshooting
- Port 5432 em uso? `docker ps` para ver containers
- PostgreSQL recusando? Aguarde 10s após `docker-compose up`
- Tests falhando? Rodá `docker-compose down && docker-compose up -d`

