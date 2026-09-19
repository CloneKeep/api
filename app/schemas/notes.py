from pydantic import BaseModel
from typing import Optional, Dict, List
from datetime import datetime
from uuid import UUID

# 1. 공통 기본 스키마
class NoteBase(BaseModel):
    title: Optional[str] = None
    type: str = "general"  # DB 모델에서 nullable=False이므로 기본값 지정 혹은 필수값 처리
    position: int = 0
    color: Optional[str] = None
    is_pinned: Optional[bool] = False
    is_archived: Optional[bool] = False
    is_trashed: Optional[bool] = False

# 2. 노트 생성 시 요청받는 스키마
class NoteCreate(NoteBase):
    id: UUID              # id: int 에서 nid: UUID로 수정
    user_id: UUID              # 작성자 ID (외래키 필수값)

# 3. 노트 수정 시 요청받는 스키마
class NoteUpdate(BaseModel):  # 모든 필드를 선택적으로 수정 가능하도록 분리
    title: Optional[str] = None
    type: Optional[str] = None
    position: Optional[int] = None
    color: Optional[str] = None
    is_pinned: Optional[bool] = None
    is_archived: Optional[bool] = None
    is_trashed: Optional[bool] = None

# 4. DB 응답 스키마
class NoteResponse(NoteBase):
    id: UUID              # id: int 에서 nid: UUID로 수정
    user_id: UUID
    created_at: datetime
    updated_at: datetime

# 본문(Body)으로 숨겨서 받을 유저 ID 구조
class UserNotesRequest(BaseModel):
    uid: UUID

# 최하단 콘텐츠 정보
class ContentDetail(BaseModel):
    text: str
    status: int
    c_pos: int

# 유저 ID 내부 데이터 구조
class UserNoteDetails(BaseModel):
    email: List[str]
    title_name: str
    note_type: str
    note_position: int
    contents: Dict[UUID, ContentDetail]  # {cid: ContentDetail}

# 최종 응답 형태: { "user_uuid": UserNoteData }
ComplexNoteResponse = List[Dict[UUID, UserNoteDetails]]

