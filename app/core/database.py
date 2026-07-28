import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

load_dotenv()

# 환경 변수 'DATABASE_URL' 사용 (GCP/GitHub Actions에서 주입)
user = os.getenv("DB_USER")
match = os.getenv("DB_PASS")
host = os.getenv("DB_HOST")
port = os.getenv("DB_PORT")
name = os.getenv("DB_NAME")

# 필수 환경변수 중 하나라도 누락되었는지 검증 로직 수정
if not all([user, match, host, port, name]):
    raise ValueError("DB 연결에 필요한 필수 환경 변수(DB_USER, DB_PASS 등)가 설정되지 않았습니다.")

# SQLAlchemy 연결 URL 조합
SQLALCHEMY_DATABASE_URL = f"postgresql://{user}:{match}@{host}:{port}/{name}"


# SQLAlchemy 엔진 및 세션 설정
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# FastAPI 전용 DB 세션 의존성 함수
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

