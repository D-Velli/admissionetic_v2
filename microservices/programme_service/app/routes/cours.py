from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.database import get_db
from app import schemas, crud

router = APIRouter()


# --------- LISTE / LECTURE ---------

@router.get("/", response_model=List[schemas.CoursRead])
def list_courses(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    """Lister les cours (pagination simple)."""
    return crud.get_courses(db, skip=skip, limit=limit)


@router.get("/{course_id}", response_model=schemas.CoursRead)
def get_course(course_id: int, db: Session = Depends(get_db)):
    """Récupérer un cours par ID."""
    course = crud.get_course(db, course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course


@router.get("/programme/{programme_id}", response_model=List[schemas.CoursRead])
def get_courses_by_programme(programme_id: int, db: Session = Depends(get_db)):
    """Lister les cours d’un programme donné."""
    return crud.get_courses_by_programme(db, programme_id)


# --------- CREATION ---------

@router.post(
    "/",
    response_model=schemas.CoursRead,
    status_code=status.HTTP_201_CREATED,
)
def create_course(course: schemas.CoursCreate, db: Session = Depends(get_db)):
    """
    Créer un cours.
    - Vérifie que le programme existe
    - Garantit l'unicité de codeCours
    """
    programme = crud.get_programme(db, course.programme_id)
    if not programme:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Programme not found for given programme_id",
        )
        
    existing = crud.get_course_by_code(db, course.codeCours)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Course with this code already exists",
        )

    try:
        return crud.create_course(db, course)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Course with this code already exists",
        )



# --------- MISE A JOUR ---------

@router.patch("/{course_id}", response_model=schemas.CoursRead)
def update_course(
    course_id: int,
    course_update: schemas.CoursUpdate,
    db: Session = Depends(get_db),
):
    """Mettre à jour un cours."""
    updated = crud.update_course(db, course_id, course_update)
    if not updated:
        raise HTTPException(status_code=404, detail="Course not found")
    return updated


# --------- SUPPRESSION ---------

@router.delete(
    "/{course_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_course(course_id: int, db: Session = Depends(get_db)):
    """Supprimer un cours."""
    deleted = crud.delete_course(db, course_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Course not found")
    # 204 => pas de body
