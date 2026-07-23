from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID

from app.schemas.users import UserCreate
from app.utils import hash_password
from app.repositories import users as user_repo  # Repository 호출

# 신규 회원가입 비즈니스 로직
def register_user(db: Session, payload: UserCreate):
    # 1. 이메일 중복 체크
    existing_user = user_repo.get_user_by_email(db, payload.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="이미 등록된 이메일입니다."
        )
    
    # 2. 데이터 가공 및 패스워드 암호화
    user_data = payload.model_dump()
    plain_password = user_data.pop("password")
    hashed_password = hash_password(plain_password)
    
    # 3. DB 저장 요청 후 결과 반환
    return user_repo.create_user(db, user_data, hashed_password)


# 유저 정보 단건 조회 비즈니스 로직
def get_user_profile(db: Session, uid: UUID):
    db_user = user_repo.get_user_by_uid(db, uid)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="존재하지 않는 유저입니다."
        )
    return db_user

