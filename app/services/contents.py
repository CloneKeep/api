from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID
from app import schemas
from app.repositories import contents as content_repo

# 콘텐츠 생성 로직 위임
def create_new_content(db: Session, payload: schemas.ContentCreate):
    return content_repo.create_content(db, payload)

# 콘텐츠 목록 전체 조회 로직 위임
def get_contents_list(db: Session, skip: int, limit: int):
    return content_repo.get_contents(db, skip, limit)

# 단건 상세 조회 및 존재 여부 검증
def get_content_detail(db: Session, cid: UUID):
    db_content = content_repo.get_content_by_cid(db, cid)
    if not db_content:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="요청하신 콘텐츠를 찾을 수 없습니다."
        )
    return db_content

# 콘텐츠 수정 처리 및 존재 여부 검증
def modify_content(db: Session, cid: UUID, payload: schemas.ContentUpdate):
    db_content = content_repo.update_content(db, cid, payload)
    if not db_content:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="수정하려는 콘텐츠가 존재하지 않습니다."
        )
    return db_content

# 콘텐츠 삭제 처리 및 존재 여부 검증
def remove_content(db: Session, cid: UUID):
    db_content = content_repo.get_content_by_cid(db, cid)
    if not db_content:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="삭제하려는 콘텐츠를 찾을 수 없습니다."
        )
    content_repo.delete_content(db, db_content)

