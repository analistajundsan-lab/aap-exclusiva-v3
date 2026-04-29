from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthCredentials
from config import settings
from models import User, SessionLocal

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_tokens(user_id: int) -> tuple[str, str]:
    access_payload = {
        "sub": str(user_id),
        "exp": datetime.utcnow() + timedelta(minutes=settings.JWT_EXPIRATION_MINUTES)
    }
    refresh_payload = {
        "sub": str(user_id),
        "exp": datetime.utcnow() + timedelta(days=7)
    }
    
    access_token = jwt.encode(access_payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    refresh_token = jwt.encode(refresh_payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    
    return access_token, refresh_token

async def get_current_user(credentials: HTTPAuthCredentials = Depends(security)) -> User:
    try:
        payload = jwt.decode(credentials.credentials, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        user_id: int = int(payload.get("sub"))
        if user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    
    db = SessionLocal()
    user = db.query(User).filter(User.id == user_id).first()
    db.close()
    
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    
    return user
