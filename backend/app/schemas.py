from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    email: str

    class Config:
        from_attributes = True


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
        from_attributes = True


class Job(BaseModel):
    company: str
    role: str
    status: str
    date: str


class UserProfileOut(BaseModel):
    id: int
    email: str
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
