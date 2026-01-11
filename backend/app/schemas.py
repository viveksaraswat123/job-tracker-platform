from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    role: Optional[str] = "job_seeker"


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    email: str
    role: str
    name: Optional[str] = None
    avatar: Optional[str] = None

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


class JobCreate(BaseModel):
    title: str
    company: str
    description: str
    location: str
    salary_min: Optional[float] = None
    salary_max: Optional[float] = None
    job_type: str
    requirements: Optional[str] = None


class JobOut(JobCreate):
    id: int
    posted_at: datetime

    class Config:
        from_attributes = True


class ApplicationCreate(BaseModel):
    job_id: int
    cover_letter: Optional[str] = None
    resume_url: Optional[str] = None


class ApplicationOut(BaseModel):
    id: int
    status: str
    applied_at: datetime
    cover_letter: Optional[str] = None
    resume_url: Optional[str] = None
    job: JobOut

    class Config:
        from_attributes = True


class Job(BaseModel):
    company: str
    role: str
    status: str
    date: str


class UserProfileOut(BaseModel):
    id: int
    email: str
    role: str
    name: str | None = None
    phone: str | None = None
    skills: str | None = None
    location: str | None = None
    linkedin: str | None = None
    github: str | None = None
    portfolio: str | None = None
    avatar: str | None = None
    resume: str | None = None

    class Config:
        from_attributes = True


class UserProfileUpdate(BaseModel):
    name: str | None = None
    phone: str | None = None
    skills: str | None = None
    location: str | None = None
    linkedin: str | None = None
    github: str | None = None
    portfolio: str | None = None
