from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings

# Create SQLAlchemy engine
connect_args = {"check_same_thread": settings.sqlite_check_same_thread} if settings.database_url.startswith("sqlite") else {}
engine = create_engine(settings.database_url, connect_args=connect_args, echo=False)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Declarative base for ORM models
Base = declarative_base()

def get_db():
    """
    Provide a database session per request.
    Close when request is finished.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
