from sqlalchemy.orm import Session
from . import models, schemas

# ------------ Programme ------------

def get_programmes(db: Session):
    return db.query(models.Programme).all()


def get_programme(db: Session, programme_id: int):
    return (
        db.query(models.Programme)
        .filter(models.Programme.id == programme_id)
        .first()
    )


def create_programme(db: Session, data: schemas.ProgrammeCreate):
    programme = models.Programme(**data.model_dump())
    db.add(programme)
    db.commit()
    db.refresh(programme)
    return programme


def update_programme(db: Session):
    pass

def delete_programme(db: Session, programme_id: int):
    pass


# ------------ Course ------------

def get_cours(db: Session):
    return db.query(models.Cours).all()


def get_cours(db: Session, cours_id: int):
    return (
        db.query(models.Cours)
        .filter(models.Cours.id == cours_id)
        .first()
    )


def create_cours(db: Session, data: schemas.CoursCreate):
    course = models.Course(**data.model_dump())
    db.add(course)
    db.commit()
    db.refresh(course)
    return course

def update_cours(db: Session):
    pass

def delete_cours(db: Session, cours_id: int):
    pass
