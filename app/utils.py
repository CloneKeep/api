import hashlib

def hash_password(password: str) -> str:
    """
    날것의 문자열 비밀번호를 받아 SHA-256 해시값(텍스트)으로 변환합니다.
    """
    # hashlib은 바이트(bytes) 단위를 입력받으므로 string을 utf-8로 인코딩해야 합니다.
    password_bytes = password.encode('utf-8')
    
    # SHA-256 해시 객체 생성 및 업데이트
    sha256_hash = hashlib.sha256(password_bytes)
    
    # 최종적으로 16진수 문자열(Hex 정렬)로 반환합니다.
    return sha256_hash.hexdigest()

