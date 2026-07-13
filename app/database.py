from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# dotenv 모둘

from  dotenv import load_dotenv

load_dotenv()

# 환경 변수 'DATABASE_URL' 사용 (GCP/GitHub Actions에서 주입)
user = os.getenv("DB_USER")
match = os.getenv("DB_PASS")
host = os.getenv("DB_HOST")
port = os.getenv("DB_PORT")
name = os.getenv("DB_NAME")

SQLALCHEMY_DATABASE_URL = f"postgresql://{user}:{match}@{host}:{port}/{name}"


# 
if not SQLALCHEMY_DATABASE_URL:
    raise ValueError("DB_URL 환경 변수 설정 안됨")

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# FastAPI에서 DB 세션을 사용할 때 호출할 함수
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

