# 1. 파이썬 이미지 선택
FROM python:3.12-slim

# 2. 작업 디렉토리 설정
WORKDIR /app

# 3. 라이브러리 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. 코드 전체 복사
COPY . .

# 5. FastAPI 실행(GCP Cloud Run, 기본포트 : 8080)
# GCP 설정 시 필요한 설정 외 다른 포트 Close)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
