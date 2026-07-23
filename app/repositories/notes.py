from sqlalchemy.orm import Session
from sqlalchemy import func
from uuid import UUID
from app.models import Note, User, Hierarchy, Content
from app.schemas.notes import NoteCreate, NoteUpdate

# 새로운 노트 생성 후 DB 저장
def create_note(db: Session, payload: NoteCreate) -> Note:
    db_note = Note(**payload.model_dump())
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note

# 전체 노트 목록 페이징 조회
def get_notes(db: Session, skip: int, limit: int) -> list[Note]:
    return db.query(Note).offset(skip).limit(limit).all()

# 고유 ID 기반 노트 단건 조회
def get_note_by_nid(db: Session, nid: UUID) -> Note | None:
    return db.query(Note).filter(Note.nid == nid).first()

# 유저 ID를 기반으로 노트 메타데이터와 하위 콘텐츠들을 구조화된 JSON 데이터로 복합 조회
def get_user_notes_summary_json(db: Session, uid: UUID) -> list:
    json_structure = func.json_build_object(
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

    query_results = (
        db.query(json_structure)
        .join(Note, User.uid == Note.uid)
        .join(Hierarchy, Note.nid == Hierarchy.nid)
        .join(Content, Hierarchy.cid == Content.cid)
        .filter(User.uid == uid)
        .group_by(User.uid, User.email, Note.title, Note.type, Note.n_pos)
        .all()
    )

    # 튜플 형태의 결과 행에서 첫 번째 요소(JSON 객체)만 추출하여 반환
    return [row[0] for row in query_results]

# 노트의 선택적 필드 수정 및 반영
def update_note(db: Session, nid: UUID, payload: NoteUpdate) -> Note | None:
    query = db.query(Note).filter(Note.nid == nid)
    db_note = query.first()
    
    if not db_note:
        return None
        
    update_data = payload.model_dump(exclude_unset=True)
    query.update(update_data)
    db.commit()
    db.refresh(db_note)
    return db_note

# 노트 레코드 영구 삭제
def delete_note(db: Session, db_note: Note) -> None:
    db.delete(db_note)
    db.commit()

