from fastapi import APIRouter, HTTPException, status, Depends, Header, Request
from sqlalchemy.orm import Session
from jose import JWTError, jwt
import hashlib
import re
from models import User, get_db
from schemas import LoginRequest, TokenResponse, UserCreate, UserResponse
from auth import hash_password, verify_password, create_tokens
from config import settings
from rate_limit import rate_limit, get_remaining_requests
from metrics_middleware import auth_metrics, rate_limit_metric
from models import AuditLog

router = APIRouter(prefix="/auth", tags=["auth"])


def hash_cpf(cpf: str) -> str:
    cpf_clean = re.sub(r"\D", "", cpf)
    return hashlib.sha256(cpf_clean.encode()).hexdigest()[:16]


def get_client_ip(request: Request) -> str:
    if x_forwarded_for := request.headers.get("x-forwarded-for"):
        return x_forwarded_for.split(",")[0].strip()
    return request.client.host if request.client else "unknown"


@router.post("/login", response_model=TokenResponse)
async def login(request: LoginRequest, req: Request, db: Session = Depends(get_db)):
    client_ip = get_client_ip(req)
    
    if not await rate_limit(f"login:{client_ip}", max_requests=5, window_seconds=60):
        await rate_limit_metric("/auth/login")
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Muitas tentativas de login. Tente novamente em 1 minuto."
        )
    
    cpf_hash = hash_cpf(request.cpf)
    user = db.query(User).filter(User.cpf_hash == cpf_hash).first()

    if not user or not verify_password(request.password, user.password_hash):
        await auth_metrics(False)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciais inválidas")

    if not user.is_active:
        await auth_metrics(False)
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Usuário inativo")

    access_token, refresh_token = create_tokens(user.id)
    await auth_metrics(True)
    return TokenResponse(access_token=access_token, refresh_token=refresh_token)


@router.post("/register", response_model=UserResponse)
async def register(request: UserCreate, req: Request, db: Session = Depends(get_db)):
    client_ip = get_client_ip(req)
    
    if not await rate_limit(f"register:{client_ip}", max_requests=10, window_seconds=3600):
        await rate_limit_metric("/auth/register")
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Muitos registros do mesmo IP. Tente novamente mais tarde."
        )
    
    cpf_hash = hash_cpf(request.cpf)

    existing = db.query(User).filter(User.cpf_hash == cpf_hash).first()
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="CPF já cadastrado")

    user = User(
        cpf_hash=cpf_hash,
        email=request.email,
        name=request.name,
        password_hash=hash_password(request.password),
        role=request.role,
    )
    db.add(user)
    db.flush()  # garante user.id antes do AuditLog
    db.add(AuditLog(user_id=user.id, action="REGISTER", resource="user"))
    db.commit()
    db.refresh(user)
    return user


@router.post("/refresh", response_model=TokenResponse)
async def refresh(
    authorization: str = Header(...),
    db: Session = Depends(get_db),
):
    try:
        scheme, token = authorization.split(" ", 1)
        if scheme.lower() != "bearer":
            raise ValueError
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        user_id = int(payload.get("sub"))
    except (JWTError, ValueError, AttributeError):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")

    user = db.query(User).filter(User.id == user_id, User.is_active == True).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuário não encontrado")

    access_token, refresh_token = create_tokens(user.id)
    return TokenResponse(access_token=access_token, refresh_token=refresh_token)


@router.post("/password-reset-request")
async def request_password_reset(email: str, req: Request, db: Session = Depends(get_db)):
    client_ip = get_client_ip(req)
    
    if not await rate_limit(f"pwd_reset:{client_ip}", max_requests=3, window_seconds=3600):
        await rate_limit_metric("/auth/password-reset-request")
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Muitas solicitações. Tente novamente em 1 hora."
        )
    
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return {"message": "Se o email existir, um link de reset será enviado"}
    
    return {"message": "Link de reset enviado para o email"}


@router.post("/password-reset")
async def reset_password(
    token: str,
    new_password: str,
    db: Session = Depends(get_db)
):
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        user_id = int(payload.get("sub"))
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido ou expirado")
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado")
    
    user.password_hash = hash_password(new_password)
    db.add(AuditLog(user_id=user_id, action="PASSWORD_RESET", resource="user"))
    db.commit()
    
    return {"message": "Senha alterada com sucesso"}

