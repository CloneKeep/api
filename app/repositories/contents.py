from sqlalchemy.orm import Session
from uuid import UUID
from app import models, schemas

# 새로운 콘텐츠 생성 후 DB 저장
def create_content(db: Session, payload: schemas.ContentCreate) -> models.Content:
    db_content = models.Content(**payload.model_dump())
    db.add(db_content)
    db.commit()
    db.refresh(db_content)
    return db_content

# 콘텐츠 전체 목록 페이징 조회
def get_contents(db: Session, skip: int, limit: int) -> list[models.Content]:
    return db.query(models.Content).offset(skip).limit(limit).all()

# 고유 ID 기반 콘텐츠 단건 조회
def get_content_by_cid(db: Session, cid: UUID) -> models.Content | None:
    return db.query(models.Content).filter(models.Content.cid == cid).first()

# 콘텐츠 선택적 수정 및 반영
def update_content(db: Session, cid: UUID, payload: schemas.ContentUpdate) -> models.Content | None:
    query = db.query(models.Content).filter(models.Content.cid == cid)
    db_content = query.first()
    
    if not db_content:
        return None
        
    query.update(payload.model_dump(exclude_unset=True))
    db.commit()
    db.refresh(db_content)
    return db_content

# 콘텐츠 레코드 완전히 영구 삭제
def delete_content(db: Session, db_content: models.Content) -> None:
    db.delete(db_content)
    db.commit()

