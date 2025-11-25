import os
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from pathlib import Path
from dotenv import load_dotenv

from app.core.security import decode_token


BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env_programme")

USER_SERVICE_URL = os.getenv("USER_SERVICE_URL")
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f"{USER_SERVICE_URL}/auth/login"  # URL du login de user_service (juste pour la doc)
)


def get_current_admin(token: str = Depends(oauth2_scheme)) -> dict:
    """
    Vérifie le JWT et s'assure que role == ADMIN.
    Retourne le payload (sub, role, etc.).
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = decode_token(token)
    except JWTError:
        raise credentials_exception

    user_id = payload.get("sub")
    role = payload.get("role")

    if user_id is None or role is None:
        raise credentials_exception

    if role != "ADMIN":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )

    return payload  # contient au moins sub, role
