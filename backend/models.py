from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum, func, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import enum
from datetime import datetime
from config import settings

Base = declarative_base()

class UserRole(str, enum.Enum):
    OPERATOR = "operator"
    SUPERVISOR = "supervisor"
    ADMIN = "admin"

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    cpf_hash = Column(String(255), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True, index=True)
    name = Column(String(255), nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(Enum(UserRole), default=UserRole.OPERATOR)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

class Incident(Base):
    __tablename__ = "incidents"
    
    id = Column(Integer, primary_key=True, index=True)
    prefix_code = Column(String(10), nullable=False, index=True)
    incident_type = Column(String(50), nullable=False)
    description = Column(String(500))
    line = Column(String(50))
    direction = Column(String(50))
    created_by = Column(Integer, nullable=False)
    created_at = Column(DateTime, server_default=func.now(), index=True)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

class Swap(Base):
    __tablename__ = "swaps"
    
    id = Column(Integer, primary_key=True, index=True)
    vehicle_out = Column(String(10), nullable=False)
    vehicle_in = Column(String(10), nullable=False)
    lines_covered = Column(String(500))
    created_by = Column(Integer, nullable=False)
    created_at = Column(DateTime, server_default=func.now(), index=True)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

class AuditLog(Base):
    __tablename__ = "audit_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    action = Column(String(50), nullable=False)
    resource = Column(String(50), nullable=False)
    resource_id = Column(Integer)
    details = Column(String(500))
    created_at = Column(DateTime, server_default=func.now(), index=True)

engine = create_engine(settings.DATABASE_URL, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
