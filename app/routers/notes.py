from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from uuid import UUID
from typing import List

from app.database import get_db
from app.models import Note, User, Hierarchy, Content  # 또는 프로젝트 import 규칙에 맞게 경로 수정 가능 (from app import models)
from app.schemas.notes import NoteCreate, NoteUpdate, NoteResponse, ComplexNoteResponse, UserNotesRequest

router = APIRouter(
    prefix="/notes",
    tags=["Notes"]
)

@router.post("/", response_model=NoteResponse, status_code=status.HTTP_201_CREATED,
             summary="새 노트 생성", description="새로운 메모 노트를 기본 정보와 함께 생성합니다.")
def create_note(payload: NoteCreate, db: Session = Depends(get_db)):
    db_note = Note(**payload.model_dump())
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note


@router.get("/", response_model=list[NoteResponse],
            summary="모든 노트 목록 조회", description="시스템에 등록된 전체 노트 목록을 기본 정렬 상태로 반환합니다.")
def read_notes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    notes = db.query(Note).offset(skip).limit(limit).all()
    return notes


@router.get("/{nid}", response_model=NoteResponse,
            summary="특정 노트 상세 조회", description="노트 ID(UUID)를 기반으로 단일 노트 정보를 상세히 조회합니다.")
def read_note(nid: UUID, db: Session = Depends(get_db)):
    db_note = db.query(Note).filter(Note.nid == nid).first()
    if not db_note:
        raise HTTPException(status_code=404, detail="요청하신 노트를 찾을 수 없습니다.")
    return db_note


@router.post("/me", response_model=ComplexNoteResponse,
            summary="유저별 노트 상세 요약 (리스트 형태)", 
            description="유저 ID를 기반으로 각 노트별 메타데이터와 하위 콘텐츠들을 리스트 형태로 반환합니다.")
def get_my_notes(request_data: UserNotesRequest, db: Session = Depends(get_db)):
    query_results = (
        db.query(
            func.json_build_object(
                User.uid, func.json_build_object(
                    'email', func.json_build_array(User.email),
                    'title_name', Note.title,
                    'note_type', Note.type,
                    'note_position', Note.n_pos,
                    'contents', func.json_object_agg(
                        Hierarchy.cid,
                        func.json_build_object(
                            'text', Content.content,
                            'status', Content.status,
                            'c_pos', Hierarchy.c_pos
                        )
                    )
                )
            )
        )
        .join(Note, User.uid == Note.uid)
        .join(Hierarchy, Note.nid == Hierarchy.nid)
        .join(Content, Hierarchy.cid == Content.cid)
        .filter(User.uid == request_data.uid)
        .group_by(User.uid, User.email, Note.title, Note.type, Note.n_pos)
        .all()
    )
    final_response = [row[0] for row in query_results]

    return final_response


@router.put("/{nid}", response_model=NoteResponse,
            summary="노트 정보 수정", description="노트 ID(UUID)를 받아 선택한 필드들을 수정합니다. 수정자 식별 정보(updated_id)가 포함되어야 합니다.")
def update_note(nid: UUID, payload: NoteUpdate, db: Session = Depends(get_db)):
    query = db.query(Note).filter(Note.nid == nid)
    db_note = query.first()
    
    if not db_note:
        raise HTTPException(status_code=404, detail="수정하려는 노트를 찾을 수 없습니다.")
        
    # 값이 들어온(변경을 요청한) 필드만 골라서 업데이트
    update_data = payload.model_dump(exclude_unset=True)
    query.update(update_data)
    db.commit()
    db.refresh(db_note)
    return db_note


@router.delete("/{nid}", status_code=status.HTTP_204_NO_CONTENT,
               summary="노트 삭제", description="노트 ID(UUID)에 해당하는 노트를 데이터베이스에서 완전히 영구 삭제합니다.")
def delete_note(nid: UUID, db: Session = Depends(get_db)):
    db_note = db.query(Note).filter(Note.nid == nid).first()
    if not db_note:
        raise HTTPException(status_code=404, detail="삭제하려는 노트를 찾을 수 없습니다.")
        
    db.delete(db_note)
    db.commit()
    return None

