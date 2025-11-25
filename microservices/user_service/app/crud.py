# app/crud.py
from typing import Sequence

from sqlalchemy.orm import Session
from sqlalchemy import func

from . import models, schemas
from .core.security import get_password_hash


# -----------------------------
# Lectures
# -----------------------------
def get_user(db: Session, user_id: int) -> models.User | None:
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str) -> models.User | None:
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(
    db: Session,
    skip: int = 0,
    limit: int = 10,
) -> Sequence[models.User]:
    return (
        db.query(models.User)
        .order_by(models.User.id.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )


def count_users(db: Session) -> int:
    return db.query(func.count(models.User.id)).scalar() or 0


# -----------------------------
# Création
# -----------------------------
def create_user(db: Session, user_in: schemas.UserCreate) -> models.User:
    # hash du mot de passe
    hashed_password = get_password_hash(user_in.password)

    db_user = models.User(
        email=user_in.email,
        password=hashed_password,
        prenom=user_in.prenom,
        nom=user_in.nom,
        role=user_in.role,
        is_active=user_in.is_active,
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


# -----------------------------
# Update
# -----------------------------
def update_user(
    db: Session,
    db_user: models.User,
    user_in: schemas.UserUpdate,
) -> models.User:
    # champs simples
    if user_in.email is not None:
        db_user.email = user_in.email
    if user_in.prenom is not None:
        db_user.prenom = user_in.prenom
    if user_in.nom is not None:
        db_user.nom = user_in.nom
    if user_in.role is not None:
        db_user.role = user_in.role
    if user_in.is_active is not None:
        db_user.is_active = user_in.is_active

    # changement de mot de passe
    if user_in.password:
        db_user.password = get_password_hash(user_in.password)

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


# -----------------------------
# Suppression / désactivation
# -----------------------------
def deactivate_user(db: Session, db_user: models.User) -> models.User:
    db_user.is_active = False
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, db_user: models.User) -> None:
    db.delete(db_user)
    db.commit()
