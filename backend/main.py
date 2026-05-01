from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging
import time
from config import settings
from models import Base, engine
from routes_auth import router as auth_router
from routes_incidents import router as incidents_router
from routes_swaps import router as swaps_router
from rate_limit import init_redis
from metrics_middleware import metrics_middleware
from prometheus_client import make_asgi_app

logging.basicConfig(level=settings.LOG_LEVEL)
logger = logging.getLogger(__name__)

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.API_TITLE,
    version=settings.API_VERSION,
    description="Sistema Operacional de Frota - Exclusiva Turismo"
)

# Mount Prometheus metrics endpoint
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def add_metrics(request: Request, call_next):
    return await metrics_middleware(request, call_next)

@app.middleware("http")
async def add_request_id_and_timing(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    duration_ms = round((time.time() - start) * 1000)
    response.headers["X-Response-Time"] = f"{duration_ms}ms"
    logger.info("%s %s %d %dms", request.method, request.url.path, response.status_code, duration_ms)
    return response

@app.on_event("startup")
async def startup():
    init_redis()

app.include_router(auth_router)
app.include_router(incidents_router)
app.include_router(swaps_router)

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.get("/ready")
async def ready():
    return {"status": "ready"}

@app.get("/")
async def root():
    return {
        "app": settings.API_TITLE,
        "version": settings.API_VERSION,
        "status": "running"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
