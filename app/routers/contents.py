from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID
from typing import List

from ..database import get_db
from .. import models, schemas

router = APIRouter(
    prefix="/contents",
    tags=["contents"]
)

# CREATE
@router.post("/", response_model=schemas.ContentResponse, status_code=status.HTTP_201_CREATED)
def create_content(payload: schemas.ContentCreate, db: Session = Depends(get_db)):
    """
    Content 생성  
    ```
    payload={  
      "content": "string",  
      "status": 0,  
      "created_id": "string",  
      "updated_id": "string"  
    }
    ```
    """
    db_content = models.Content(**payload.model_dump())
    db.add(db_content)
    db.commit()
    db.refresh(db_content)
    return db_content

# READ ALL
@router.get("/", response_model=list[schemas.ContentResponse])
def read_contents(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Content 전체조회  
    skip : 조회 시작 인덱스 설정, 기본값 skip=0  
    limit: 마지막 조회 인덱스 설정, 기본값 limit=100
    """
    contents = db.query(models.Content).offset(skip).limit(limit).all()
    return contents

# READ ONE
@router.get("/{cid}", response_model=schemas.ContentResponse)
def read_content(cid: UUID, db: Session = Depends(get_db)):
    """
    특정 Content 조회
    """
    db_content = db.query(models.Content).filter(models.Content.cid == cid).first()
    if not db_content:
        raise HTTPException(status_code=404, detail="Content not found")
    return db_content

# UPDATE
@router.put("/{cid}", response_model=schemas.ContentResponse)
def update_content(cid: UUID, payload: schemas.ContentUpdate, db: Session = Depends(get_db)):
    """
    특정 Content 수정
    """
    query = db.query(models.Content).filter(models.Content.cid == cid)
    db_content = query.first()
    
    if not db_content:
        raise HTTPException(status_code=404, detail="Content not found")
        
    query.update(payload.model_dump(exclude_unset=True))
    db.commit()
    db.refresh(db_content)
    return db_content

# DELETE
@router.delete("/{cid}", status_code=status.HTTP_204_NO_CONTENT)
def delete_content(cid: UUID, db: Session = Depends(get_db)):
    """
    특정 Content 삭제
    """
    db_content = db.query(models.Content).filter(models.Content.cid == cid).first()
    if not db_content:
        raise HTTPException(status_code=404, detail="Content not found")
        
    db.delete(db_content)
    db.commit()
    return None

