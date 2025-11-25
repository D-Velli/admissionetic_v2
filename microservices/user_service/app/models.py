from .database import Base
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum as SAEnum
from sqlalchemy.sql import func
from enum import Enum as PyEnum


class RoleEnum(str, PyEnum):
    ADMIN = "ADMIN"
    USER = "USER"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password = Column(String(255), nullable=False)
    prenom = Column(String(100), nullable=True)
    nom = Column(String(100), nullable=True)
    role = Column(
        SAEnum(RoleEnum, name="role_enum"),
        nullable=False,
        default=RoleEnum.USER,
    )
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime(timezone=True), default=func.now())
