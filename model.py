import string
from typing import Optional
from uuid import UUID, uuid4
from pydantic import BaseModel, Field
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Article(BaseModel):
    id: Optional[UUID] = Field(default_factory=uuid4)
    numero: str
    designation: str
    qc: int
    qpc: int


class ArticleUpdateRequest(BaseModel):
    numero: Optional[str]
    designation: Optional[str]
    qc: Optional[int]
    qpc: Optional[int]


class Users(BaseModel):
    id: int
    firstname: str
    lastname: str
    address: str


class UserModel(BaseModel):
    firstname: str
    lastname: str
    address: str

