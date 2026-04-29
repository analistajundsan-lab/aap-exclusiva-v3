import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/aap_db"
    REDIS_URL: str = "redis://localhost:6379/0"
    JWT_SECRET_KEY: str = "your-secret-key-change-in-production"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION_MINUTES: int = 30
    API_TITLE: str = "AAP Exclusiva v3.0"
    API_VERSION: str = "3.0.0"
    ENVIRONMENT: str = "development"
    LOG_LEVEL: str = "INFO"
    ALLOWED_ORIGINS: list = ["http://localhost:5173", "http://localhost:3000"]

    class Config:
        env_file = ".env"

settings = Settings()
