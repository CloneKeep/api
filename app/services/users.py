from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID

from app.schemas.users import UserCreate, UserLogin
from app.utils import password_hash, verify_password, create_access_token
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

    # 3. [보안 핵심] DB에서 꺼낸 유저의 고유 uid를 토큰의 'sub' 키에 바인딩하여 생성
    access_token = create_access_token(data={"sub": str(user.uid)})

    # 4. 규격에 맞게 토큰 반환
    return {"access_token": access_token, "token_type": "bearer"}
