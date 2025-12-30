from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from .database import Base


class ApplicationStatus(str, enum.Enum):
    applied = "Applied"
    interview = "Interview"
    rejected = "Rejected"
    offer = "Offer"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    applications = relationship(
        "Application",
        back_populates="owner",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<User id={self.id} email={self.email}>"


class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)
    company = Column(String(150), nullable=False)
    role = Column(String(150), nullable=False)
    status = Column(
        Enum(ApplicationStatus),
        default=ApplicationStatus.applied,
        nullable=False
    )
    applied_on = Column(DateTime, default=datetime.utcnow)

    owner_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )

    owner = relationship("User", back_populates="applications")

    def __repr__(self):
        return f"<Application id={self.id} company={self.company} role={self.role} status={self.status}>"
