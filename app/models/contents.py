from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Text, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

from app.core.database import Base

class Content(Base):
    __tablename__ = "contents_dup"

    # 기본키 및 외래키 설정
    id      = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    note_id = Column(UUID(as_uuid=True), ForeignKey("notes_dup.id"), nullable=False)

    # 기본 content 정보 컬럼
    content     = Column(Text)
    position    = Column(Integer, nullable=False, default=0)
    is_checked  = Column(Boolean, nullable=True, default=False)

    # 생성 및 수정 메타데이터 정보
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())

    # ORM 관계 설정 (User 모델과의 연결)
    note = relationship("Note", back_populates="contents")

