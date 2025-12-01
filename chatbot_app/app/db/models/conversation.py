from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func
from app.db.session import Base

class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    message = Column(String, nullable=False)
    response = Column(String, nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
