import os
from datetime import datetime, timedelta, timezone
from pathlib import Path
from fastapi import Header, HTTPException, status

from dotenv import load_dotenv
from jose import jwt, JWTError
from passlib.context import CryptContext

# === Chargement .env_user ===
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env_user")

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
INTERNAL_API_TOKEN = os.getenv("INTERNAL_API_TOKEN")


if not SECRET_KEY:
    raise RuntimeError("SECRET_KEY is not set. Check your .env_user file.")

# === Contexte de hash de mot de passe ===
pwd_context = CryptContext(schemes=["bcrypt_sha256"], deprecated="auto")


def get_password_hash(password: str) -> str:
    """Hash un mot de passe en clair."""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Vérifie qu'un mot de passe en clair correspond au hash stocké."""
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(
    data: dict,
    expires_delta: timedelta | None = None,
) -> str:
    """
    Crée un JWT signé contenant `data`.
    On ajoute automatiquement `exp`.
    """
    to_encode = data.copy()

    if expires_delta is None:
        expires_delta = timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))

    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_token(token: str) -> dict:
    """
    Décode un JWT et renvoie le payload.
    Lève JWTError si le token est invalide / expiré.
    """
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    return payload


# Cette fonction est /users/{user_id}
def verify_internal_token(x_internal_token: str = Header(...)):
    if not INTERNAL_API_TOKEN or x_internal_token != INTERNAL_API_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden",
        )
