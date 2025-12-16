from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class ApplicationCreate(BaseModel):
    company: str
    role: str
    status: str


class ApplicationOut(ApplicationCreate):
    id: int

    class Config:
        orm_mode = True
