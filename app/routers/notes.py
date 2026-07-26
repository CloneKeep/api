from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from uuid import UUID

from app.database import get_db
from app.schemas.notes import NoteCreate, NoteUpdate, NoteResponse, ComplexNoteResponse, UserNotesRequest
from app.services import notes as note_service
from app.dependencies import get_current_user_id

router = APIRouter(
    prefix="/notes",
    tags=["Notes"],
    dependencies=[Depends(get_current_user_id)] # JWT 인증 의존성 주입
)

@router.post("/", response_model=NoteResponse, status_code=status.HTTP_201_CREATED,
             summary="새 노트 생성", description="새로운 메모 노트를 기본 정보와 함께 생성합니다.")
def create_note(payload: NoteCreate, db: Session = Depends(get_db)):
    return note_service.create_new_note(db=db, payload=payload)


@router.get("/", response_model=list[NoteResponse],
            summary="모든 노트 목록 조회", description="시스템에 등록된 전체 노트 목록을 기본 정렬 상태로 반환합니다.")
def read_notes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return note_service.get_notes_list(db=db, skip=skip, limit=limit)


@router.get("/me", response_model=ComplexNoteResponse,
            summary="유저별 노트 상세 요약 (리스트 형태)", 
            description="유저 ID를 기반으로 각 노트별 메타데이터와 하위 콘텐츠들을 리스트 형태로 반환합니다.")
def get_my_notes(current_uid: str = Depends(get_current_user_id), db: Session = Depends(get_db)):
    return note_service.get_my_notes_summary(db=db, user_id=current_uid)


@router.get("/{nid}", response_model=NoteResponse,
            summary="특정 노트 상세 조회", description="노트 ID(UUID)를 기반으로 단일 노트 정보를 상세히 조회합니다.")
def read_note(nid: UUID, db: Session = Depends(get_db)):
    return note_service.get_note_detail(db=db, nid=nid)


@router.put("/{nid}", response_model=NoteResponse,
            summary="노트 정보 수정", description="노트 ID(UUID)를 받아 선택한 필드들을 수정합니다. 수정자 식별 정보(updated_id)가 포함되어야 합니다.")
def update_note(nid: UUID, payload: NoteUpdate, db: Session = Depends(get_db)):
    return note_service.modify_note(db=db, nid=nid, payload=payload)


@router.delete("/{nid}", status_code=status.HTTP_204_NO_CONTENT,
               summary="노트 삭제", description="노트 ID(UUID)에 해당하는 노트를 데이터베이스에서 완전히 영구 삭제합니다.")
def delete_note(nid: UUID, db: Session = Depends(get_db)):
    note_service.remove_note(db=db, nid=nid)
    return None

