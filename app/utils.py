from datetime import datetime, timedelta, timezone
from typing import Optional
import jwt
from passlib.context import CryptContext

from app.auth_config import auth_settings # JWT 보안 세팅값

# 비밀번호 암호화 컨텍스트 설정 (bcrypt 알고리즘 사용)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 비밀번호 해싱 함수 (회원가입 시 사용)
def password_hash(password: str) -> str:
    return pwd_context.hash(password)

# 비밀번호 검증 함수 (로그인 시 사용)
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# JWT 엑세스 토큰 발행 함수
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()

    # 만료 시간(exp) 계산 (별도 설정이 없으면 auth_settings의 30분 적용)
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=auth_settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    # 만료 시간을 토큰 데이터(Payload)에 주입
    to_encode.update({"exp": expire})

    # auth_config에 설정된 비밀키와 알고리즘으로 서명하여 외계어 문자열(JWT) 완성
    encoded_jwt = jwt.encode(to_encode, auth_settings.JWT_SECRET_KEY, algorithm=auth_settings.ALGORITHM)
    return encoded_jwt

