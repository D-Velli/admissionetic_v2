from sqlalchemy.orm import Session

from . import models, schemas


# --------- Admissions ---------

def list_admissions(db: Session):
    return db.query(models.Admission).all()


def get_admission(db: Session, admission_id: int):
    return (
        db.query(models.Admission)
        .filter(models.Admission.id == admission_id)
        .first()
    )


def list_admissions_by_user(db: Session, user_id: int):
    return (
        db.query(models.Admission)
        .filter(models.Admission.user_id == user_id)
        .all()
    )


def create_admission(db: Session, data: schemas.AdmissionCreate, user_id: int):
    admission = models.Admission(user_id=user_id, **data.model_dump())
    db.add(admission)
    db.commit()
    db.refresh(admission)
    return admission


def update_admission_status(
    db: Session,
    admission_id: int,
    data: schemas.AdmissionStatusUpdate,
):
    admission = get_admission(db, admission_id)
    if not admission:
        return None

    admission.statut = data.statut
    if data.commentaire is not None:
        admission.commentaire = data.commentaire

    db.commit()
    db.refresh(admission)
    return admission


def delete_admission(db: Session, admission_id: int):
    admission = get_admission(db, admission_id)
    if not admission:
        return False
    db.delete(admission)
    db.commit()
    return True
