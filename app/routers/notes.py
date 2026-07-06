from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
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
    # 1. DB에서 4개 테이블 조인 및 정렬하여 데이터 조회
    query_results = (
        db.query(User, Note, Hierarchy, Content)
        .join(Note, User.uid == Note.uid)
        .join(Hierarchy, Note.nid == Hierarchy.nid)
        .join(Content, Hierarchy.cid == Content.cid)
        .filter(User.uid == request_data.uid)
        .order_by(Note.nid, Hierarchy.c_pos.asc(), Content.status.asc())
        .all()
    )

    if not query_results:
        raise HTTPException(status_code=404, detail="요청하신 유저의 노트 데이터를 찾을 수 없습니다.")

    # 2. 중간 조립을 위한 임시 딕셔너리 구조 { nid: { 유저노트데이터 } }
    note_group = {}

    for user_obj, note_obj, hierarchy_obj, content_obj in query_results:
        # 노트 ID(nid)별로 그룹을 묶어줍니다 (DB에서 2줄이 나오면 2개의 그룹이 생김)
        if note_obj.nid not in note_group:
            note_group[note_obj.nid] = {
                "uid": user_obj.uid,
                "email": [user_obj.email],
                "title_name": note_obj.title,
                "note_type": note_obj.type,
                "note_position": note_obj.n_pos,
                "contents": {}
            }
        
        # 해당 노트 그룹의 contents 내부에 하위 콘텐츠를 하나씩 추가
        note_group[note_obj.nid]["contents"][hierarchy_obj.cid] = {
            "text": content_obj.content,
            "status": content_obj.status,
            "c_pos": hierarchy_obj.c_pos
        }

    # 3. 임시로 묶은 그룹들을 원하는 최종 JSON 리스트 형태로 변환
    final_response = []
    for nid, data in note_group.items():
        # "유저ID": { 데이터 } 구조로 만들어서 리스트에 append
        formatted_item = {
            data["uid"]: {
                "email": data["email"],
                "title_name": data["title_name"],
                "note_type": data["note_type"],
                "note_position": data["note_position"],
                "contents": data["contents"]
            }
        }
        final_response.append(formatted_item)

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

