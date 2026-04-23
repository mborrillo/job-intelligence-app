from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    name: str
    email: Optional[EmailStr] = None
    skills: Optional[str] = None
    keywords: Optional[str] = None


class UserCreate(UserBase):
    pass


class UserRead(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class JobBase(BaseModel):
    title: str
    description: Optional[str] = None
    url: str
    company: Optional[str] = None
    location: Optional[str] = None
    source: Optional[str] = "jooble"
    score: int


class JobRead(JobBase):
    id: int
    user_id: int
    run_id: Optional[int] = None
    found_at: datetime
    is_active: bool

    class Config:
        from_attributes = True


class RunBase(BaseModel):
    status: str = "running"
    source: str = "jooble"


class RunCreate(RunBase):
    pass


class RunRead(RunBase):
    id: int
    started_at: datetime
    finished_at: Optional[datetime] = None

    class Config:
        from_attributes = True
