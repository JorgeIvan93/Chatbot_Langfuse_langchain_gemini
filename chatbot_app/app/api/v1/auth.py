from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException
from jose import jwt
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.core.config import settings
from app.db.session import get_db
from app.db.models.user import User
from app.services.security import verify_password

# Router for authentication endpoints
router = APIRouter(prefix="/api/v1/auth", tags=["Authentication"])


class LoginRequest(BaseModel):
    """
    Login payload with username and password.
    """

    username: str
    password: str


def create_access_token(subject: str) -> str:
    """
    Create JWT token with expiration using SECRET_KEY and ALGORITHM from settings.
    """
    expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
    payload = {"sub": subject, "exp": expire}
    return jwt.encode(payload, settings.secret_key, algorithm=settings.algorithm)


@router.post("/token", summary="Login and get JWT token")
async def login(data: LoginRequest, db: Session = Depends(get_db)):
    """
    Authenticate user from database and return JWT token.
    """
    user = db.query(User).filter(User.username == data.username).first()
    if not user or not verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    token = create_access_token(subject=user.username)
    return {"access_token": token, "token_type": "bearer"}
