from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

# 상대 경로 대신 안전한 절대 경로 사용
from app.core.database import Base

class Note(Base):
    __tablename__ = "notes_dup"

    # 기본키 및 외래키 설정
    id      = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users_dup.id"), nullable=False)
    
    # 기본 note 정보 컬럼
    title    = Column(String, nullable=False)
    type     = Column(String, nullable=False, default="general")
    position = Column(Integer, nullable=False, default=0)
    color    = Column(String, nullable=True)
    
    # 상태 및 커스텀 기능 컬럼
    is_pinned   = Column(Boolean, nullable=True, default=False)
    is_archived = Column(Boolean, nullable=True, default=False)
    is_trashed  = Column(Boolean, nullable=True, default=False)
    
    # 생성 및 수정 메타데이터 정보
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())

    # Content 모델과의 1:N 관계 정의
    contents = relationship("Content", back_populates="note")

    # ORM 관계 설정 (User 모델과의 연결)
    user = relationship("User", back_populates="notes")

