from sqlalchemy.orm import Session
from uuid import UUID
from app.models.users import User

# 이메일로 사용자 조회
def get_user_by_email(db: Session, email: str) -> User | None:
    return db.query(User).filter(User.email == email).first()

# UUID로 사용자 조회
def get_user_by_uid(db: Session, uid: UUID) -> User | None:
    return db.query(User).filter(User.uid == uid).first()

# 새로운 사용자 레코드 생성
def create_user(db: Session, user_data: dict, hashed_password: str) -> User:
    db_user = User(**user_data, pw_hash=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

