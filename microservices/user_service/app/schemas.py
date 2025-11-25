# app/schemas.py
from datetime import datetime
from enum import Enum

from pydantic import BaseModel, EmailStr, constr


# -----------------------------
# Enums
# -----------------------------
class RoleEnum(str, Enum):
    ADMIN = "ADMIN"
    USER = "USER"


# -----------------------------
# Schemas User
# -----------------------------
class UserBase(BaseModel):
    email: EmailStr
    prenom: str | None = None
    nom: str | None = None
    role: RoleEnum = RoleEnum.USER
    is_active: bool = True


class UserCreate(UserBase):
    # Reçu en clair, sera hashé côté backend
    password: constr(min_length=8, max_length=64)


class UserUpdate(BaseModel):
    # Ce que l’admin ou l’utilisateur peut modifier
    email: EmailStr | None = None
    prenom: str | None = None
    nom: str | None = None
    role: RoleEnum | None = None
    is_active: bool | None = None
    password: str | None = None  


class UserRead(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class UserInDB(UserRead):
    # Utilisation interne (auth, vérif de mot de passe)
    hashed_password: str


class UserList(BaseModel):
    total: int
    items: list[UserRead]


# -----------------------------
# Schemas Auth
# -----------------------------
class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    # Contenu du JWT après décodage
    sub: str | None = None  # user id ou email
    exp: int | None = None  # timestamp d’expiration
