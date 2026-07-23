from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from uuid import UUID

from ..database import get_db
from .. import schemas
from ..services import contents as content_service

router = APIRouter(
    prefix="/contents",
    tags=["Contents"]
)

@router.post("/", response_model=schemas.ContentResponse, status_code=status.HTTP_201_CREATED,
             summary="새 메모 콘텐츠 생성", 
             description="새로운 메모 본문(콘텐츠)을 생성합니다. 텍스트 내용과 초기 상태값을 데이터베이스에 기록합니다.")
def create_content(payload: schemas.ContentCreate, db: Session = Depends(get_db)):
    return content_service.create_new_content(db=db, payload=payload)


@router.get("/", response_model=list[schemas.ContentResponse],
            summary="메모 콘텐츠 목록 전체 조회", 
            description="시스템에 등록된 모든 메모 콘텐츠 목록을 페이징 처리하여 한 번에 조회합니다.")
def read_contents(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return content_service.get_contents_list(db=db, skip=skip, limit=limit)


@router.get("/{cid}", response_model=schemas.ContentResponse,
            summary="특정 메모 콘텐츠 상세 조회", 
            description="콘텐츠 고유 ID(cid)를 기반으로 단일 메모 본문의 상세 정보를 정확하게 찾아 조회합니다.")
def read_content(cid: UUID, db: Session = Depends(get_db)):
    return content_service.get_content_detail(db=db, cid=cid)


@router.put("/{cid}", response_model=schemas.ContentResponse,
            summary="특정 메모 콘텐츠 수정", 
            description="콘텐츠 고유 ID(cid)를 받아 본문 내용이나 상태 정보 등을 선택적으로 변경합니다.")
def update_content(cid: UUID, payload: schemas.ContentUpdate, db: Session = Depends(get_db)):
    return content_service.modify_content(db=db, cid=cid, payload=payload)


@router.delete("/{cid}", status_code=status.HTTP_204_NO_CONTENT,
               summary="특정 메모 콘텐츠 영구 삭제", 
               description="콘텐츠 고유 ID(cid)에 해당하는 메모 본문 레코드를 데이터베이스에서 완전히 영구 삭제합니다.")
def delete_content(cid: UUID, db: Session = Depends(get_db)):
    content_service.remove_content(db=db, cid=cid)
    return None

