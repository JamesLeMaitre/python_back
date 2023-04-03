from typing import Optional, Type

from sqlalchemy.orm import Session

from app.core.security import get_password_hash, verify_password
from app.crud.base import CRUDBase, ModelType
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate

from sqlalchemy import and_


def get_by_email(db: Session, *, email: str) -> Optional[User]:
    return db.query(User).filter(and_(User.email == email, not User.disabled)).first()


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    def __init__(self, model: Type[ModelType]):
        super().__init__(model)
        self.hashed_password = None

    def create(self, db: Session, *, obj: UserCreate) -> User:
        db_obj = User(
            email=obj.email,
            hashed_password=get_password_hash(obj.password),
            full_name=obj.full_name,
            username=obj.username
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


def authenticate(self, db: Session, *, email: str, password: str) -> Optional[User]:
    current_user = get_by_email(db, email=email)
    if not current_user:
        return None
    if not verify_password(password, current_user.hashed_password):
        return None
    return current_user


getUser = CRUDUser(User)
