# 🚌 AAP Exclusiva — Sistema de Gestão de Frota v3.0

Sistema completo de gestão de frota com **FastAPI** + **React** + **Docker**, incluindo autenticação JWT, CRUD de ocorrências e trocas, observabilidade com Prometheus/Grafana, e CI/CD automatizado.

---

## 🏗️ Arquitetura

```
┌─────────────────────────────────────────────────┐
│                    Internet                      │
└──────────────────────┬──────────────────────────┘
                       │
              ┌────────▼────────┐
              │  Frontend (80)   │  React + Vite + Tailwind
              │  nginx:alpine    │  Port 5173 (ext)
              └────────┬────────┘
                       │ /api/*
              ┌────────▼────────┐
              │  Backend (8000) │  FastAPI + SQLAlchemy
              │  Python 3.11    │  JWT Auth + Rate Limiting
              └──┬──────────┬───┘
                 │          │
        ┌────────▼─┐  ┌─────▼──────┐
        │ PostgreSQL│  │   Redis    │
        │  Port 5432│  │  Port 6379 │
        └───────────┘  └────────────┘
                 │
        ┌────────▼─────────┐
        │   Prometheus     │  Port 9090
        │   + Grafana      │  Port 3001
        └──────────────────┘
```

---

## 🚀 Quick Start (Docker)

```bash
# 1. Clone e configure ambiente
git clone <repo-url>
cd aap-exclusiva
cp .env.example .env
# Edite .env com sua JWT_SECRET_KEY

# 2. Suba todos os serviços
docker compose up -d

# 3. Acesse
#   Frontend:   http://localhost:5173
#   API Docs:   http://localhost:8000/docs
#   Prometheus: http://localhost:9090
#   Grafana:    http://localhost:3001  (admin/admin)
```

---

## 💻 Desenvolvimento Local (sem Docker)

### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Configure .env
export DATABASE_URL="sqlite:///./dev.db"
export JWT_SECRET_KEY="dev-secret-key"

# Inicie
uvicorn main:app --reload --port 8000
```

### Frontend
```bash
cd frontend
npm install
npm run dev
# Acesse: http://localhost:5173
```

---

## 🧪 Testes

```bash
# Backend - todos os testes com cobertura
cd <raiz>
pytest tests/ -v --cov=backend --cov-report=term-missing

# Resultado esperado: 40/40 PASSED, ~79% coverage
```

---

## 📡 API Reference

### Autenticação
| Método | Endpoint | Descrição |
|--------|----------|-----------|
| POST | `/auth/register` | Cadastra novo usuário |
| POST | `/auth/login` | Login — retorna JWT token |
| GET | `/auth/me` | Dados do usuário atual |

### Ocorrências
| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/incidents/` | Lista todas (paginado) |
| POST | `/incidents/` | Cria nova ocorrência |
| GET | `/incidents/{id}` | Detalhes de uma ocorrência |
| PUT | `/incidents/{id}` | Atualiza ocorrência |
| DELETE | `/incidents/{id}` | Remove ocorrência |

### Trocas de Veículos
| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/swaps/` | Lista todas (paginado) |
| POST | `/swaps/` | Cria nova troca |
| GET | `/swaps/{id}` | Detalhes de uma troca |
| PUT | `/swaps/{id}` | Atualiza troca |
| DELETE | `/swaps/{id}` | Remove troca |

### Observabilidade
| Endpoint | Descrição |
|----------|-----------|
| `GET /health` | Health check |
| `GET /metrics` | Métricas Prometheus |

---

## 🔐 Autenticação

Todas as rotas protegidas requerem o header:
```
Authorization: Bearer <jwt_token>
```

### Roles disponíveis:
- **ADMIN** — acesso total (CRUD + auditoria)
- **SUPERVISOR** — cria, edita e deleta qualquer registro
- **OPERATOR** — cria e edita apenas seus próprios registros

---

## 📊 Observabilidade

### Métricas disponíveis (Prometheus):
- `http_requests_total` — total de requisições por método/endpoint/status
- `http_request_duration_seconds` — latência das requisições
- `active_users_total` — usuários ativos
- `incidents_created_total` — ocorrências criadas
- `swaps_created_total` — trocas criadas

### Grafana:
- URL: http://localhost:3001
- Usuário: `admin` / Senha: `admin`
- Dashboard pré-configurado em `infra/grafana-dashboard.json`

---

## 🗂️ Estrutura do Projeto

```
aap-exclusiva/
├── backend/               # FastAPI app
│   ├── main.py            # App entry point + health check
│   ├── models.py          # SQLAlchemy models
│   ├── schemas.py         # Pydantic schemas
│   ├── auth.py            # JWT authentication
│   ├── config.py          # Settings
│   ├── routes_auth.py     # Auth endpoints
│   ├── routes_incidents.py# Incidents CRUD
│   ├── routes_swaps.py    # Swaps CRUD
│   ├── observability.py   # Prometheus metrics
│   ├── middleware.py       # Request logging
│   ├── rate_limit.py      # Rate limiting
│   └── requirements.txt
├── frontend/              # React + Vite + Tailwind
│   ├── src/
│   │   ├── api/           # Axios client
│   │   ├── components/    # IncidentTable, SwapTable, etc.
│   │   ├── hooks/         # useAuth, useIncidents, useSwaps
│   │   ├── pages/         # Login, Dashboard, Incidents, Swaps
│   │   └── store/         # Zustand auth store
│   ├── Dockerfile         # nginx multi-stage build
│   └── package.json
├── tests/                 # pytest suite (40 tests, ~79% coverage)
├── infra/                 # prometheus.yml, grafana dashboard
├── docker-compose.yml     # Full stack dev environment
├── docker-compose.prod.yml# Production overrides
└── .env.example           # Environment template
```

---

## 🔄 CI/CD

Pipeline GitHub Actions (`.github/workflows/ci-cd.yml`):

1. **Test** — pytest com coverage report
2. **Build** — Docker images backend + frontend
3. **Push** — GitHub Container Registry
4. **Deploy** — docker compose pull & up (production)

---

## 📝 Variáveis de Ambiente

| Variável | Padrão | Descrição |
|----------|--------|-----------|
| `DATABASE_URL` | — | PostgreSQL connection string |
| `JWT_SECRET_KEY` | — | **Obrigatório** em produção |
| `JWT_ALGORITHM` | `HS256` | Algoritmo JWT |
| `JWT_EXPIRATION_MINUTES` | `60` | Expiração do token |
| `REDIS_HOST` | `localhost` | Host do Redis |
| `REDIS_PORT` | `6379` | Porta do Redis |
| `ENVIRONMENT` | `development` | Ambiente atual |

---

## 📜 Licença

MIT © AAP Exclusiva 2024
