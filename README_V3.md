# AAP Exclusiva v3.0

**Status**: Phase 1 Foundation (In Progress)  
**Version**: 3.0.0  
**Last Update**: 29 April 2026

## Quick Start

### Local Development (5 min)

```bash
# Setup
python3.12 -m venv venv
source venv/bin/activate  # Linux/Mac
pip install -r backend/requirements.txt

# Docker services
docker-compose up -d

# Run API
cd backend && uvicorn main:app --reload

# Swagger UI
http://localhost:8000/docs
```

### Running Tests
```bash
pytest tests/ -v --cov=backend
```

## Roadmap

- **Phase 1** (In Progress): Foundation (Auth + DB + Tests)
- **Phase 2**: API Core (CRUD endpoints)
- **Phase 3**: Observability (Prometheus + Grafana)
- **Phase 4**: Frontend (React UI)
- **Phase 5**: DevOps (K8s + CI/CD)

## Architecture

```
Frontend (React 18)
    ↓ REST API
FastAPI Backend (Python 3.12)
    ↓ SQL
PostgreSQL 15 + Redis 7
```

## Technology Stack

- **Backend**: FastAPI, SQLAlchemy, Pydantic, JWT
- **Database**: PostgreSQL 15, Redis 7
- **Testing**: Pytest, Coverage
- **CI/CD**: GitHub Actions
- **Container**: Docker, Docker Compose

## Development

- Lint: `flake8 backend`
- Format: `black backend`
- Test: `pytest tests/ -v`
- Coverage: `pytest tests/ --cov=backend --cov-report=html`

## Documentation

- [SETUP.md](./SETUP.md) - Local development setup
- [Architecture](./ARQUITECTURA_PROPOSTA.md) - Full technical specification
- [Roadmap](./ROADMAP_EXECUTIVO.md) - 10-week execution plan

## Status

✅ **Phase 1.1**: Infrastructure base  
✅ **Phase 1.2**: Authentication & Security  
⏳ **Phase 2**: API Core endpoints (Next)

---

*AAP Exclusiva — Sistema Operacional de Frota v3.0*
