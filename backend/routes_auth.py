from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
import hashlib
import re
from models import User, SessionLocal, get_db
from schemas import LoginRequest, TokenResponse, UserCreate, UserResponse
from auth import hash_password, verify_password, create_tokens

router = APIRouter(prefix="/auth", tags=["auth"])

def hash_cpf(cpf: str) -> str:
    cpf_clean = re.sub(r'\D', '', cpf)
    return hashlib.sha256(cpf_clean.encode()).hexdigest()[:16]

@router.post("/login", response_model=TokenResponse)
async def login(request: LoginRequest, db: Session = Depends(get_db)):
    cpf_hash = hash_cpf(request.cpf)
    user = db.query(User).filter(User.cpf_hash == cpf_hash).first()
    
    if not user or not verify_password(request.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciais inválidas")
    
    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Usuário inativo")
    
    access_token, refresh_token = create_tokens(user.id)
    return TokenResponse(access_token=access_token, refresh_token=refresh_token)

@router.post("/register", response_model=UserResponse)
async def register(request: UserCreate, db: Session = Depends(get_db)):
    cpf_hash = hash_cpf(request.cpf)
    
    existing = db.query(User).filter(User.cpf_hash == cpf_hash).first()
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="CPF já cadastrado")
    
    user = User(
        cpf_hash=cpf_hash,
        email=request.email,
        name=request.name,
        password_hash=hash_password(request.password),
        role=request.role
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@router.post("/refresh", response_model=TokenResponse)
async def refresh(db: Session = Depends(get_db)):
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Not implemented yet")
