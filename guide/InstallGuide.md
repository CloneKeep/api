### 윈도우11 파이썬 설치(git bash 사용)
```
winget install -e --id Python.Python.3.12
```
1. 윈도우 "앱 실행 별칭" 끄기 (필수)
설정 > 앱 > 앱 실행 별칭 > 앱 설치 관리자(python.exe, python3.exe)
목록을 아래로 내려서 python.exe와 python3.exe를 찾으세요.
그 두 개의 스위치를 모두 **[켬 -> 끔(Off)]**으로 바꿉니다.

2. 버전확인
```
python --version
```
3. 가상 환경 만들기
```
# 가상 환경 만들기 (python 대신 py 사용)
py -m venv venv

# 가상 환경 활성화 (이후에는 python 명령어 사용 가능)
source venv/Scripts/activate

# FastAPI 설치
pip install fastapi "uvicorn[standard]"

# 테스트 코드 작성(main.py)
echo "from fastapi import FastAPI

app = FastAPI()

@app.get('/')
def root():
    return {'message': 'FastAPI 설치가 완료되었습니다!'}" > main.py

# 서버 실행
uvicorn main:app --reload
```
### 결과 확인
  1. 브라우저를 열고 주소창에 http://127.0.0.1:8000 을 입력해 보세요.
    {"message": "FastAPI 설치가 완료되었습니다!"}가 보이면 성공!
  2. 대화형 API 문서: http://127.0.0.1:8000/docs 에 접속해 보세요.(swagger 페이지)
