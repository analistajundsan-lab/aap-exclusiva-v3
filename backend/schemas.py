from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from enum import Enum

class UserRole(str, Enum):
    OPERATOR = "operator"
    SUPERVISOR = "supervisor"
    ADMIN = "admin"

class UserCreate(BaseModel):
    cpf: str = Field(..., min_length=11, max_length=11)
    email: EmailStr
    name: str = Field(..., min_length=3, max_length=255)
    password: str = Field(..., min_length=8)
    role: UserRole = UserRole.OPERATOR

class UserResponse(BaseModel):
    id: int
    email: str
    name: str
    role: UserRole
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

class LoginRequest(BaseModel):
    cpf: str = Field(..., min_length=11, max_length=11)
    password: str

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class IncidentCreate(BaseModel):
    prefix_code: str = Field(..., min_length=1, max_length=10)
    incident_type: str
    description: str = Field(None, max_length=500)
    line: str = None
    direction: str = None

class IncidentResponse(BaseModel):
    id: int
    prefix_code: str
    incident_type: str
    description: str
    line: str
    direction: str
    created_by: int
    created_at: datetime

    class Config:
        from_attributes = True

class SwapCreate(BaseModel):
    vehicle_out: str = Field(..., min_length=1, max_length=10)
    vehicle_in: str = Field(..., min_length=1, max_length=10)
    lines_covered: str = Field(None, max_length=500)

class SwapResponse(BaseModel):
    id: int
    vehicle_out: str
    vehicle_in: str
    lines_covered: str
    created_by: int
    created_at: datetime

    class Config:
        from_attributes = True
