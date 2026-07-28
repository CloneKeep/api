import os
from dotenv import load_dotenv

load_dotenv()

# CORS 및 네트워크 설정
ALLOWED_ORIGINS = [
    "https://integrationschedulerproject.github.io",  # GitHub Pages 주소
    "http://localhost:8081",                          # 로컬 테스트용 (FastAPI)
]

# 인증 및 보안 설정
class JwtSettings:
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY") # JWT 비밀키
    ALGORITHM: str = "HS256"                          # JWT 암호화 알고리즘
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30             # 토큰 만료시간, 30분 설정

    # .env에 키가 누락되었을 경우 서버 실행 차단
    def __init__(self):
        if not self.JWT_SECRET_KEY:
            raise ValueError(".env 파일에 'JWT_SECRET_KEY'가 설정되지 않았습니다. 보안을 위해 서버를 시작할 수 없습니다.")

# 다른 파일에서 불러와서 사용할 수 있도록 인스턴스 생성
jwt_settings = JwtSettings()

