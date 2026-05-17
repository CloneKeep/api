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
    db_content = models.Content(**payload.model_dump())
    db.add(db_content)
    db.commit()
    db.refresh(db_content)
    return db_content

# READ ALL
@router.get("/", response_model=list[schemas.ContentResponse])
def read_contents(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    contents = db.query(models.Content).offset(skip).limit(limit).all()
    return contents

# READ ONE
@router.get("/{cid}", response_model=schemas.ContentResponse)
def read_content(cid: UUID, db: Session = Depends(get_db)):
    db_content = db.query(models.Content).filter(models.Content.cid == cid).first()
    if not db_content:
        raise HTTPException(status_code=404, detail="Content not found")
    return db_content

# UPDATE
@router.put("/{cid}", response_model=schemas.ContentResponse)
def update_content(cid: UUID, payload: schemas.ContentUpdate, db: Session = Depends(get_db)):
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
    db_content = db.query(models.Content).filter(models.Content.cid == cid).first()
    if not db_content:
        raise HTTPException(status_code=404, detail="Content not found")
        
    db.delete(db_content)
    db.commit()
    return None

