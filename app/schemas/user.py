from pydantic import BaseModel, EmailStr
from typing import List, Optional
from app.schemas.summary import SummaryOut


class UserBase(BaseModel):
    username: str
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserLogin(BaseModel):
    username: str
    password: str


class UserOut(UserBase):
    id: int
    is_admin: bool

    class Config:
        orm_mode = True


class UserWithSummaries(UserOut):
    summaries: List[SummaryOut] = []
