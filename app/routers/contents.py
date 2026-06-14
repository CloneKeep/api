from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID
from typing import List

from ..database import get_db
from .. import models, schemas

router = APIRouter(
    prefix="/contents",
    tags=["Contents"]
)

@router.post("/", response_model=schemas.ContentResponse, status_code=status.HTTP_201_CREATED,
             summary="새 메모 콘텐츠 생성", 
             description="새로운 메모 본문(콘텐츠)을 생성합니다. 텍스트 내용과 초기 상태값을 데이터베이스에 기록합니다.")
def create_content(payload: schemas.ContentCreate, db: Session = Depends(get_db)):
    db_content = models.Content(**payload.model_dump())
    db.add(db_content)
    db.commit()
    db.refresh(db_content)
    return db_content


@router.get("/", response_model=list[schemas.ContentResponse],
            summary="메모 콘텐츠 목록 전체 조회", 
            description="시스템에 등록된 모든 메모 콘텐츠 목록을 페이징 처리하여 한 번에 조회합니다.")
def read_contents(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    contents = db.query(models.Content).offset(skip).limit(limit).all()
    return contents


@router.get("/{cid}", response_model=schemas.ContentResponse,
            summary="특정 메모 콘텐츠 상세 조회", 
            description="콘텐츠 고유 ID(cid)를 기반으로 단일 메모 본문의 상세 정보를 정확하게 찾아 조회합니다.")
def read_content(cid: UUID, db: Session = Depends(get_db)):
    db_content = models.Content
    db_content = db.query(models.Content).filter(models.Content.cid == cid).first()
    if not db_content:
        raise HTTPException(status_code=404, detail="요청하신 콘텐츠를 찾을 수 없습니다.")
    return db_content


@router.put("/{cid}", response_model=schemas.ContentResponse,
            summary="특정 메모 콘텐츠 수정", 
            description="콘텐츠 고유 ID(cid)를 받아 본문 내용이나 상태 정보 등을 선택적으로 변경합니다.")
def update_content(cid: UUID, payload: schemas.ContentUpdate, db: Session = Depends(get_db)):
    query = db.query(models.Content).filter(models.Content.cid == cid)
    db_content = query.first()
    
    if not db_content:
        raise HTTPException(status_code=404, detail="수정하려는 콘텐츠가 존재하지 않습니다.")
        
    query.update(payload.model_dump(exclude_unset=True))
    db.commit()
    db.refresh(db_content)
    return db_content


@router.delete("/{cid}", status_code=status.HTTP_204_NO_CONTENT,
               summary="특정 메모 콘텐츠 영구 삭제", 
               description="콘텐츠 고유 ID(cid)에 해당하는 메모 본문 레코드를 데이터베이스에서 완전히 영구 삭제합니다.")
def delete_content(cid: UUID, db: Session = Depends(get_db)):
    db_content = db.query(models.Content).filter(models.Content.cid == cid).first()
    if not db_content:
        raise HTTPException(status_code=404, detail="삭제하려는 콘텐츠를 찾을 수 없습니다.")
        
    db.delete(db_content)
    db.commit()
    return None
