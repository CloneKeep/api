from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from uuid import UUID

from app.core.database import get_db
from app.schemas.users import UserCreate, UserResponse, UserLogin, Token # , UserProfileResponse
from app.services import users as user_service  # Service 호출

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED,
             summary="신규 유저 생성(회원가입)", description="새로운 사용자 계정을 생성합니다. 이메일 중복을 체크합니다.")
def create_user(payload: UserCreate, db: Session = Depends(get_db)):
    return user_service.register_user(db=db, payload=payload)


@router.get("/{uid}", response_model=UserResponse,
            summary="유저 정보 단건 조회", description="유저 ID(UUID)를 기반으로 특정 사용자의 프로필 정보를 조회합니다.")
def read_user(uid: UUID, db: Session = Depends(get_db)):
    return user_service.get_user_profile(db=db, uid=uid)


@router.post("/login", response_model=Token,
            summary="가입 유저 로그인", description="가입 회원의 아이디와 비밀번호를 확인하고 토큰을 발급합니다.")
def user_login(login_data: UserLogin, db: Session = Depends(get_db)):
    return user_service.user_login(db=db, login_data=login_data)

