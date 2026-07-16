from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

# 상대 경로 대신 안전한 절대 경로 사용
from app.database import Base

class Note(Base):
    __tablename__ = "notes"

    # 기본키 및 외래키 설정
    nid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    uid = Column(UUID(as_uuid=True), ForeignKey("users.uid"), nullable=False)
    
    # 기본 노트 정보 컬럼
    title = Column(String, nullable=True)
    type = Column(String, nullable=False, default="general")
    n_pos = Column(Integer, default=0)
    
    # 상태 및 커스텀 기능 컬럼 (SQL 스키마 확장 반영)
    is_color = Column(String, nullable=True)       # TEXT 타입 매핑
    is_pinned = Column(Boolean, nullable=True, default=False)    # BOOLEAN 타입 매핑
    is_archived = Column(Boolean, nullable=True, default=False)  # BOOLEAN 타입 매핑
    is_trashed = Column(Boolean, nullable=True, default=False)   # BOOLEAN 타입 매핑
    
    # 생성 및 수정 메타데이터 정보
    created_at = Column(DateTime(timezone=True), default=func.now())
    created_id = Column(String, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())
    updated_id = Column(String, nullable=False)

    # ORM 관계 설정 (User 모델과의 연결)
    user = relationship("User", back_populates="notes")
    hierarchies = relationship("Hierarchy", back_populates="note")
