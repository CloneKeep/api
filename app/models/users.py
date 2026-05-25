from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

from app.database import Base

class User(Base):
    __tablename__ = "users"

    uid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, nullable=False)
    pw_hash = Column(String, nullable=False)
    
    created_at = Column(DateTime(timezone=True), default=func.now())
    created_id = Column(String, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())
    updated_id = Column(String, nullable=False)

    # Note 모델과의 1:N 관계 정의
    notes = relationship("Note", back_populates="user")

