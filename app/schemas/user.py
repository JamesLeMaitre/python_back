from typing import Optional

from pydantic import BaseModel, EmailStr

from app.models.user import User


class UserBase(BaseModel):
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = True
    username: Optional[str] = None
    full_name: Optional[str] = None


class UserInDB(User):
    hashed_password: str


class UserUpdate(UserBase):
    password: Optional[str] = None


class UserInDBBase(UserBase):
    id: Optional[int] = None

    # class Config:
    #     orm_mode = True


# Additional properties to return via API
class User(UserInDBBase):
    pass


# Properties to receive via API on creation
class UserCreate(UserBase):
    email: EmailStr
    password: str
