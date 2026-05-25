from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app import config
from app.database import get_db
from app.routers import test, contents, users, notes


app = FastAPI()

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=config.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"], # GET, POST 등 모두 허용
    allow_headers=["*"],
)

# 라우터 등록
app.include_router(test.router)
app.include_router(contents.router)
app.include_router(users.router)
app.include_router(notes.router)

