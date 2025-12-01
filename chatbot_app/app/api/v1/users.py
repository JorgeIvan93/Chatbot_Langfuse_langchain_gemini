
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, OperationalError

from app.db.session import get_db
from app.db.models.user import User
from app.schemas.user import UserCreate, UserOut
from app.services.security import hash_password
from app.services.standard_logger import logger

router = APIRouter(prefix="/api/v1/users", tags=["Users"])

@router.post("/register", response_model=UserOut, summary="Register a new user")
def register_user(payload: UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user:
    - Validate unique username.
    - Hash the password before saving.
    - Return user data (without password).
    """
    try:
        existing = db.query(User).filter(User.username == payload.username).first()
        if existing:
            raise HTTPException(status_code=400, detail="Username is already taken")

        hashed = hash_password(payload.password)
        user = User(username=payload.username, email=payload.email, hashed_password=hashed)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    except HTTPException:
        raise

    except IntegrityError as ie:
        logger.exception(f"IntegrityError on register_user: {ie}")
        db.rollback()
        raise HTTPException(status_code=400, detail="Username or email already exists")

    except OperationalError as oe:
        logger.exception(f"OperationalError on register_user: {oe}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Database operation failed")

    except Exception as e:
        logger.exception(f"Unhandled error on register_user: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Unexpected error during registration")
