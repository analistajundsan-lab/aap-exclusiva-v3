import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

@pytest.fixture(scope="session")
def db():
    SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
    engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
    
    from models import Base
    Base.metadata.create_all(bind=engine)
    
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return SessionLocal()

@pytest.fixture
def client():
    from main import app
    from models import get_db
    
    def override_get_db():
        db = None
        try:
            yield db
        finally:
            if db:
                db.close()
    
    app.dependency_overrides[get_db] = override_get_db
    return TestClient(app)

def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_ready(client):
    response = client.get("/ready")
    assert response.status_code == 200
    assert response.json()["status"] == "ready"

def test_root(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "version" in response.json()
