from datetime import datetime, timedelta, timezone
from typing import Optional
import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from passlib.context import CryptContext

from app.core.config import jwt_settings # JWT 보안 세팅값


# 비밀번호 암호화 컨텍스트 설정 (bcrypt 알고리즘 사용)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# FastAPI에서 제공하는 Bearer 헤더 추출기 (Authorization 헤더 자동 추적)
security = HTTPBearer()


# 비밀번호 해싱 함수 (회원가입 시 사용)
def password_hash(password: str) -> str:
    return pwd_context.hash(password)

# 비밀번호 검증 함수 (로그인 시 사용)
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# JWT 엑세스 토큰 발행 함수
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()

    # 만료 시간(exp) 계산 (별도 설정이 없으면 jwt_settings의 30분 적용)
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=jwt_settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    # 만료 시간을 토큰 데이터(Payload)에 주입
    to_encode.update({"exp": expire})

    # auth_config에 설정된 비밀키와 알고리즘으로 서명하여 외계어 문자열(JWT) 완성
    encoded_jwt = jwt.encode(to_encode, jwt_settings.JWT_SECRET_KEY, algorithm=jwt_settings.ALGORITHM)
    return encoded_jwt

# [인증 가드] 프론트엔드가 보낸 토큰을 검증하는 공통 의존성 함수
def get_current_user_id(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
    token = credentials.credentials

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="인증 자격 증명이 올바르지 않거나 유효하지 않습니다.",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        # 1. 서버의 비밀키로 토큰 복호화 및 서명 검증 (만료 시간도 자동 검증됨)
        payload = jwt.decode(token, jwt_settings.JWT_SECRET_KEY, algorithms=[jwt_settings.ALGORITHM])

        # 2. Payload의 표준 규격 키인 'sub'에서 우리가 숨겨두었던 유저의 진짜 uid 추출
        uid: str = payload.get("sub")
        if uid is None:
            raise credentials_exception

        return uid  # 검증 성공 시 uid를 API 본문 함수로 토스합니다.

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="토큰의 유효 기간이 만료되었습니다. 다시 로그인해 주세요."
        )
    except jwt.PyJWTError:
        raise credentials_exception
