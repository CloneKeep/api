from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

from app.database import Base

class Content(Base):
    __tablename__ = "contents"

    cid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    content = Column(Text)
    status = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), default=func.now())
    created_id = Column(String, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())
    updated_id = Column(String, nullable=False)

    # Hierarchy의 'cid' 외래키를 타고 들어오는 관계들
    hierarchies_as_cid = relationship(
        "Hierarchy", 
        foreign_keys="[Hierarchy.cid]", # 문자열로 명시할 때 테이블명.컬럼명 형태로 작성
        # back_populates="content"
    )
    
    # Hierarchy의 'cnt_pid' 외래키를 타고 들어오는 관계들
    hierarchies_as_pid = relationship(
        "Hierarchy", 
        foreign_keys="[Hierarchy.cnt_pid]", 
        # back_populates="parent_content"
    )
