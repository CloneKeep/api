from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID

from app.database import get_db
from app.models.users import User
from app.schemas.users import UserCreate, UserResponse

from app.utils import hash_password

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED,
             summary="신규 유저 생성(회원가입)", description="새로운 사용자 계정을 생성합니다. 이메일 중복을 체크합니다.")
def create_user(payload: UserCreate, db: Session = Depends(get_db)):
    # 이메일 중복 체크
    existing_user = db.query(User).filter(User.email == payload.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="이미 등록된 이메일입니다.")
    
    # UserCreate 데이터를 User 모델 형태로 변환 (password를 pw_hash로 매핑)
    user_data = payload.model_dump()
    plain_password = user_data.pop("password")

    # password SHA-256 암호화 처리
    hashed_password = hash_password(plain_password)
    
    # 원래는 여기서 비밀번호 해싱 알고리즘을 타야 합니다. (지금은 테스트용 임시 저장)
    db_user = User(**user_data, pw_hash=hashed_password)
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@router.get("/{uid}", response_model=UserResponse,
            summary="유저 정보 단건 조회", description="유저 ID(UUID)를 기반으로 특정 사용자의 프로필 정보를 조회합니다.")
def read_user(uid: UUID, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.uid == uid).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="존재하지 않는 유저입니다.")
    return db_user

