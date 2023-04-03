from sqlalchemy import Column, Integer, String, Boolean

from app.db.base_class import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    full_name = Column(String(50))
    email = Column(String(50), unique=True, index=True)
    hashed_password = Column(String(50))
    disabled = Column(Boolean, default=False)
