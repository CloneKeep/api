from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

from app.database import Base

class Note(Base):
    __tablename__ = "notes"

    nid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    uid = Column(UUID(as_uuid=True), ForeignKey("users.uid"), nullable=False)
    title = Column(String)
    type = Column(String, nullable=False)
    n_pos = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), default=func.now())
    created_id = Column(String, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())
    updated_id = Column(String, nullable=False)

    user = relationship("User", back_populates="notes")

