from datetime import datetime, timedelta
from typing import Optional
from fastapi import APIRouter, HTTPException
from jose import jwt
from pydantic import BaseModel
from app.core.config import settings

router = APIRouter()

# Request model for login
class LoginRequest(BaseModel):
    username: str
    password: str

# Function to create JWT token
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=settings.access_token_expire_minutes))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    return encoded_jwt

@router.post("/token", summary="Generate JWT token")
async def login(data: LoginRequest):

    # Validate username and password from .env
    if data.username != settings.auth_username or data.password != settings.auth_password:
        raise HTTPException(status_code=401, detail="Invalid username or password")

    # Create token payload
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": data.username},
        expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}