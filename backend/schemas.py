from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator
from datetime import datetime
from typing import Optional
from enum import Enum
import re


class UserRole(str, Enum):
    OPERATOR = "operator"
    SUPERVISOR = "supervisor"
    ADMIN = "admin"


class UserCreate(BaseModel):
    cpf: str = Field(..., min_length=11, max_length=14)
    email: EmailStr
    name: str = Field(..., min_length=3, max_length=255)
    password: str = Field(..., min_length=8)
    role: UserRole = UserRole.OPERATOR

    @field_validator("cpf")
    @classmethod
    def cpf_only_digits(cls, v: str) -> str:
        digits = re.sub(r"\D", "", v)
        if len(digits) != 11:
            raise ValueError("CPF deve ter 11 dígitos")
        return digits


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: str
    name: str
    role: UserRole
    is_active: bool
    created_at: datetime


class LoginRequest(BaseModel):
    cpf: str = Field(..., min_length=11, max_length=14)
    password: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class PasswordResetRequest(BaseModel):
    email: EmailStr


class PasswordReset(BaseModel):
    token: str
    new_password: str = Field(..., min_length=8)


class IncidentCreate(BaseModel):
    prefix_code: str = Field(..., min_length=1, max_length=10)
    incident_type: str
    description: Optional[str] = Field(None, max_length=500)
    line: Optional[str] = None
    direction: Optional[str] = None


class IncidentUpdate(BaseModel):
    prefix_code: Optional[str] = Field(None, min_length=1, max_length=10)
    incident_type: Optional[str] = None
    description: Optional[str] = Field(None, max_length=500)
    line: Optional[str] = None
    direction: Optional[str] = None


class IncidentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    prefix_code: str
    incident_type: str
    description: Optional[str] = None
    line: Optional[str] = None
    direction: Optional[str] = None
    created_by: int
    created_at: datetime


class SwapCreate(BaseModel):
    vehicle_out: str = Field(..., min_length=1, max_length=10)
    vehicle_in: str = Field(..., min_length=1, max_length=10)
    lines_covered: Optional[str] = Field(None, max_length=500)


class SwapUpdate(BaseModel):
    vehicle_out: Optional[str] = Field(None, min_length=1, max_length=10)
    vehicle_in: Optional[str] = Field(None, min_length=1, max_length=10)
    lines_covered: Optional[str] = Field(None, max_length=500)


class SwapResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    vehicle_out: str
    vehicle_in: str
    lines_covered: Optional[str] = None
    created_by: int
    created_at: datetime
