from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from datetime import timedelta
from uuid import UUID

from app.schemas.users import UserCreate, UserLogin
from app.core.security import password_hash, verify_password, create_token
from app.core.config import jwt_settings # JWT 보안 세팅값
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
    hashed_password = password_hash(plain_password)
    
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


# 유저 ID/PW를 확인하고 JWT 토큰 발급
def user_login(db: Session, login_data: UserLogin):
    # 1. DB에서 유저 조회 (DB 필드명에 맞게 username 또는 email 등으로 조회)
    user = user_repo.get_user_by_email(db, login_data.email)

    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="아이디 또는 비밀번호가 올바르지 않습니다.")

    # 2. 비밀번호 검증 (utils에 작성한 bcrypt 검증기 사용)
    if not verify_password(login_data.password, user.pw_hash):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="아이디 또는 비밀번호가 올바르지 않습니다.")

    return generate_token_pair(user.uid)


# 유효한 Refresh Token으로 Access Token 재발급
def refresh_access_token(db: Session, user_id: UUID):
    return generate_token_pair(user_id)


# 유저 ID/PW를 확인하고 JWT 토큰 발급
def generate_token_pair(user_id: UUID):
    # [보안 핵심] 유저의 고유 uid를 토큰의 'sub' 키에 바인딩하여 생성
    access_token = create_token(
        data={"sub": str(user_id), "type": "access"}, 
        expires_delta=timedelta(minutes=jwt_settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    refresh_token = create_token(
        data={"sub": str(user_id), "type": "refresh"}, 
        expires_delta=timedelta(days=jwt_settings.REFRESH_TOKEN_EXPIRE_DAYS)
    )

    # 규격에 맞게 토큰 반환
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

