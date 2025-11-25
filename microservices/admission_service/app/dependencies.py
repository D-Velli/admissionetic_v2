# app/dependencies.py
import os
from pathlib import Path

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from dotenv import load_dotenv

from app.core.security import decode_token


BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env_admission")

USER_SERVICE_URL = os.getenv("USER_SERVICE_URL")

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f"{USER_SERVICE_URL}/auth/login"  # utilisé pour la doc Swagger
)


def _credentials_exception() -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )


def get_current_user(token: str = Depends(oauth2_scheme)) -> dict:
    """
    Récupère le payload du JWT (user connecté).
    Retourne au minimum : {"sub": <user_id>, "role": "..."} si ton user_service encode ça.
    """
    try:
        payload = decode_token(token)
    except JWTError:
        raise _credentials_exception()

    user_id = payload.get("sub")
    if user_id is None:
        raise _credentials_exception()

    # role peut être None pour certains utilisateurs, donc on ne le force pas ici
    return payload


def get_current_admin(current_user: dict = Depends(get_current_user)) -> dict:
    """
    Vérifie que le user connecté est ADMIN.
    """
    role = current_user.get("role")

    if role != "ADMIN":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )

    return current_user  # contient au moins sub, role
