from app.db.session import Base, engine
from app.services.standard_logger import logger

def init_db():
    """
    Create all tables from ORM models on startup.
    """
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("SQLite tables created or already exist.")
    except Exception as e:
        logger.error(f"Error creating SQLite tables: {e}")
        raise
