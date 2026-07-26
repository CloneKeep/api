from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID
from app.schemas.notes import NoteCreate, NoteUpdate, UserNotesRequest
from app.repositories import notes as note_repo

# 노트 생성 로직 위임
def create_new_note(db: Session, payload: NoteCreate):
    return note_repo.create_note(db, payload)

# 노트 목록 조회 로직 위임
def get_notes_list(db: Session, skip: int, limit: int):
    return note_repo.get_notes(db, skip, limit)

# 단건 상세 조회 및 검증
def get_note_detail(db: Session, nid: UUID):
    db_note = note_repo.get_note_by_nid(db, nid)
    if not db_note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="요청하신 노트를 찾을 수 없습니다."
        )
    return db_note

# 유저별 복합 노트 요약 데이터 조회 로직 위임
def get_my_notes_summary(db: Session, user_id: UUID):
    return note_repo.get_user_notes_summary_json(db, user_id)

# 노트 수정 및 존재 여부 검증
def modify_note(db: Session, nid: UUID, payload: NoteUpdate):
    db_note = note_repo.update_note(db, nid, payload)
    if not db_note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="수정하려는 노트를 찾을 수 없습니다."
        )
    return db_note

# 노트 삭제 및 존재 여부 검증
def remove_note(db: Session, nid: UUID):
    db_note = note_repo.get_note_by_nid(db, nid)
    if not db_note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="삭제하려는 노트를 찾을 수 없습니다."
        )
    note_repo.delete_note(db, db_note)

