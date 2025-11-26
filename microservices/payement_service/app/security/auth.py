import os
from fastapi import Header, HTTPException, status, Depends
from jose import jwt, JWTError
from pathlib import Path
from dotenv import load_dotenv
from fastapi.security import OAuth2PasswordBearer
from ..config import SECRET_KEY, ALGORITHM


BASE_DIR = Path(__file__).resolve().parent.parent.parent
load_dotenv(BASE_DIR / ".env_payement")

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

def decode_token(token: str) -> dict:
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])


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



# authorizations est loche pour moi ??/
# def get_current_user(authorization: str = Header(...)) -> dict:
#     # "Bearer <token>"
#     try:
#         scheme, _, token = authorization.partition(" ")
#         if scheme.lower() != "bearer":
#             raise ValueError
#     except Exception:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Invalid authorization header",
#         )

#     try:
#         payload = decode_token(token)
#     except JWTError:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Invalid or expired token",
#         )
#     return payload
