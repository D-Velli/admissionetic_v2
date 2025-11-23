from typing import List, Optional

from sqlalchemy.orm import Session

from . import models, schemas


# ===================== PROGRAMMES =====================

def get_programmes(db: Session, skip: int = 0, limit: int = 100) -> List[models.Programme]:
    """Liste paginée des programmes."""
    return (
        db.query(models.Programme)
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_programme(db: Session, programme_id: int) -> Optional[models.Programme]:
    """Programme par ID, ou None."""
    return (
        db.query(models.Programme)
        .filter(models.Programme.id == programme_id)
        .first()
    )


def get_programme_by_code(db: Session, code: str) -> Optional[models.Programme]:
    """Programme par codeProgramme."""
    return (
        db.query(models.Programme)
        .filter(models.Programme.codeProgramme == code)
        .first()
    )


def create_programme(db: Session, data: schemas.ProgrammeCreate) -> models.Programme:
    """Création d’un programme."""
    programme = models.Programme(**data.model_dump())
    db.add(programme)
    db.commit()
    db.refresh(programme)
    return programme


def update_programme(
    db: Session,
    programme_id: int,
    data: schemas.ProgrammeUpdate,
) -> Optional[models.Programme]:
    """Mise à jour d’un programme (retourne None si non trouvé)."""
    programme = get_programme(db, programme_id)
    if not programme:
        return None

    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(programme, field, value)

    db.commit()
    db.refresh(programme)
    return programme


def delete_programme(db: Session, programme_id: int) -> bool:
    """Suppression d’un programme (True si supprimé, False sinon)."""
    programme = get_programme(db, programme_id)
    if not programme:
        return False

    db.delete(programme)
    db.commit()
    return True


# ======================= COURS ========================

def get_courses(db: Session, skip: int = 0, limit: int = 100) -> List[models.Cours]:
    """Liste paginée des cours."""
    return (
        db.query(models.Cours)
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_course(db: Session, course_id: int) -> Optional[models.Cours]:
    """Cours par ID, ou None."""
    return (
        db.query(models.Cours)
        .filter(models.Cours.id == course_id)
        .first()
    )

def get_course_by_code(db: Session, code: str) -> Optional[models.Cours]:
    """Cours par codeCours (pour vérifier les doublons)."""
    return (
        db.query(models.Cours)
        .filter(models.Cours.codeCours == code)
        .first()
    )


def get_courses_by_programme(db: Session, programme_id: int) -> List[models.Cours]:
    """Tous les cours d’un programme."""
    return (
        db.query(models.Cours)
        .filter(models.Cours.programme_id == programme_id)
        .all()
    )


def create_course(db: Session, data: schemas.CoursCreate) -> models.Cours:
    """Création d’un cours."""
    course = models.Cours(**data.model_dump())
    db.add(course)
    db.commit()
    db.refresh(course)
    return course


def update_course(
    db: Session,
    course_id: int,
    data: schemas.CoursUpdate,
) -> Optional[models.Cours]:
    """Mise à jour d’un cours (retourne None si non trouvé)."""
    course = get_course(db, course_id)
    if not course:
        return None

    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(course, field, value)

    db.commit()
    db.refresh(course)
    return course


def delete_course(db: Session, course_id: int) -> bool:
    """Suppression d’un cours."""
    course = get_course(db, course_id)
    if not course:
        return False

    db.delete(course)
    db.commit()
    return True
