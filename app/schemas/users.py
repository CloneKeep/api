from pydantic import BaseModel
from datetime import datetime
from uuid import UUID

# 1. 공통 기본 스키마
class UserBase(BaseModel):
    email: str  # EmailStr -> 유효한 이메일인지 체크하려면 해당 모듈로 변경(설치)필요

# 2. 회원가입/유저 생성 요청 스키마
class UserCreate(UserBase):
    password: str    # 클라이언트에게 날것의 비밀번호를 받음
    created_id: str
    updated_id: str

# 3. 유저 정보 응답 스키마 (보안을 위해 pw_hash 제외)
class UserResponse(UserBase):
    uid: UUID
    created_at: datetime
    created_id: str
    updated_at: datetime
    updated_id: str

    model_config = {
        "from_attributes": True
    }
