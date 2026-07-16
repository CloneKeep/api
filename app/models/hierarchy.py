from sqlalchemy import Column, Integer, DateTime, ForeignKey, Text, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

from app.database import Base

class Hierarchy(Base):
    __tablename__ = "hierarchy"

    # 기본키
    hid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # 외래키 연관 관계
    nid = Column(UUID(as_uuid=True), ForeignKey("notes.nid"), nullable=False)
    cid = Column(UUID(as_uuid=True), ForeignKey("contents.cid"), nullable=False)
    cnt_pid = Column(UUID(as_uuid=True), ForeignKey("contents.cid"), nullable=True) # NULL 허용
    
    # 위치 정보
    n_pos = Column(Integer, default=0)
    c_pos = Column(Integer, default=0)
    
    # 생성 및 수정 메타데이터
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    created_id = Column(String, nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    updated_id = Column(String, nullable=True) # 스키마에 따라 NULL 허용

    # ORM 관계(relationship) 정의 (선택 사항이지만 데이터 조회 시 매우 유용합니다)
    note = relationship("Note", back_populates="hierarchies")
    
    # Content 모델과의 관계 (★외래키가 2개이므로 foreign_keys 필수 지정★)
    content = relationship(
        "Content", 
        foreign_keys=[cid], # cid 컬럼을 기준으로 Content와 연결됨을 명시
        back_populates="hierarchies_as_cid"
    )
    
    parent_content = relationship(
        "Content", 
        foreign_keys=[cnt_pid], # cnt_pid 컬럼을 기준으로 Content와 연결됨을 명시
        back_populates="hierarchies_as_pid"
    )

