from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.database import get_db


router = APIRouter(prefix="", tags=[""])

@router.get('/')
async def root():
    content = {'message': 'FastAPI 설치가 완료되었습니다!'}
    return JSONResponse(content=content, media_type="application/json; charset=utf-8")

@router.get("/test-contents")
async def read_contents(db: Session = Depends(get_db)):
    try:
        # contents 테이블의 모든 데이터를 조회합니다.
        query = text("SELECT * FROM contents")
        result = db.execute(query).fetchall()

        # 결과를 읽기 쉬운 JSON(dict) 형태로 변환합니다.
        data = [dict(row._mapping) for row in result]

        return {"status": "success", "data": data}
    except Exception as e:
        return {"status": "error", "message": str(e)}
