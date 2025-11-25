from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.dependencies import get_current_admin
from app.database import get_db
from app import schemas, crud

router = APIRouter()


# --------- LISTE / LECTURE ---------

@router.get("/", response_model=List[schemas.ProgrammeRead])
def list_programmes(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    """Lister les programmes (pagination simple)."""
    return crud.get_programmes(db, skip=skip, limit=limit)


@router.get("/{programme_id}", response_model=schemas.ProgrammeRead)
def get_programme(programme_id: int, db: Session = Depends(get_db)):
    """Récupérer un programme par ID."""
    prog = crud.get_programme(db, programme_id)
    if not prog:
        raise HTTPException(status_code=404, detail="Programme not found")
    return prog


@router.get("/code/{code_programme}", response_model=schemas.ProgrammeRead)
def get_programme_by_code(code_programme: str, db: Session = Depends(get_db)):
    """Récupérer un programme par son codeProgramme."""
    prog = crud.get_programme_by_code(db, code_programme)
    if not prog:
        raise HTTPException(status_code=404, detail="Programme not found")
    return prog


# --------- CREATION ---------

@router.post(
    "/",
    response_model=schemas.ProgrammeRead,
    status_code=status.HTTP_201_CREATED,
)
def create_programme(
    programme: schemas.ProgrammeCreate,
    db: Session = Depends(get_db),
    admin: dict = Depends(get_current_admin)
    ):
    """Créer un programme (avec vérification d'unicité du code)."""
    existing = crud.get_programme_by_code(db, programme.codeProgramme)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Programme with this code already exists",
        )

    return crud.create_programme(db, programme)


# --------- MISE A JOUR ---------

@router.patch("/{programme_id}", response_model=schemas.ProgrammeRead)
def update_programme(
    programme_id: int,
    programme_update: schemas.ProgrammeUpdate,
    db: Session = Depends(get_db),
):
    """Mettre à jour un programme (partiel)."""
    prog = crud.update_programme(db, programme_id, programme_update)
    if not prog:
        raise HTTPException(status_code=404, detail="Programme not found")
    return prog


# --------- SUPPRESSION ---------

@router.delete(
    "/{programme_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_programme(programme_id: int, db: Session = Depends(get_db)):
    """Supprimer un programme."""
    deleted = crud.delete_programme(db, programme_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Programme not found")
    # Pas de retour pour un 204
