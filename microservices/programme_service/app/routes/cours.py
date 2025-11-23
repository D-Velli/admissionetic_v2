from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app import schemas, crud

router = APIRouter()


@router.get("/", response_model=List[schemas.CoursRead])
def list_courses(db: Session = Depends(get_db)):
    return crud.get_courses(db)


@router.post(
    "/",
    response_model=schemas.CoursRead,
    status_code=status.HTTP_201_CREATED,
)
def create_course(course: schemas.CoursCreate, db: Session = Depends(get_db)):
    return crud.create_course(db, course)


@router.get("/{course_id}", response_model=schemas.CoursRead)
def get_course(course_id: int, db: Session = Depends(get_db)):
    c = crud.get_course(db, course_id)
    if not c:
        raise HTTPException(status_code=404, detail="Course not found")
    return c
