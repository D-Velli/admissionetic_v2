from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app import schemas, crud

router = APIRouter()


@router.get("/", response_model=List[schemas.ProgrammeRead])
def list_programmes(db: Session = Depends(get_db)):
    return crud.get_programmes(db)


@router.post(
    "/",
    response_model=schemas.ProgrammeRead,
    status_code=status.HTTP_201_CREATED,
)
def create_programme(programme: schemas.ProgrammeCreate, db: Session = Depends(get_db)):
    return crud.create_programme(db, programme)


@router.get("/{programme_id}", response_model=schemas.ProgrammeRead)
def get_programme(programme_id: int, db: Session = Depends(get_db)):
    prog = crud.get_programme(db, programme_id)
    if not prog:
        raise HTTPException(status_code=404, detail="Programme not found")
    return prog
