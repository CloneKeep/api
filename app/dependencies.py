from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
from app.auth_config import auth_settings

# FastAPI에서 제공하는 Bearer 헤더 추출기 (Authorization 헤더 자동 추적)
security = HTTPBearer()

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
        payload = jwt.decode(token, auth_settings.JWT_SECRET_KEY, algorithms=[auth_settings.ALGORITHM])

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
