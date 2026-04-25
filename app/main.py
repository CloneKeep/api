from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()

@app.get('/')
def root():
    content = {'message': 'FastAPI 설치가 완료되었습니다!'}
    return JSONResponse(content=content, media_type="application/json; charset=utf-8")

