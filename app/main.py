from fastapi import FastAPI, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy import text
from database import get_db
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://integrationschedulerproject.github.io/"], # GitHub Pages 주소
    allow_credentials=True,
    allow_methods=["*"], # GET, POST 등 모두 허용
    allow_headers=["*"],
)


@app.get('/')
def root():
    content = {'message': 'FastAPI 설치가 완료되었습니다!'}
    return JSONResponse(content=content, media_type="application/json; charset=utf-8")

@app.get("/test-contents")
def read_contents(db: Session = Depends(get_db)):
    try:
        # contents 테이블의 모든 데이터를 조회합니다.
        query = text("SELECT * FROM contents")
        result = db.execute(query).fetchall()

        # 결과를 읽기 쉬운 JSON(dict) 형태로 변환합니다.
        data = [dict(row._mapping) for row in result]

        return {"status": "success", "data": data}
    except Exception as e:
        return {"status": "error", "message": str(e)}
