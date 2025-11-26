from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.models import TypeAdmissionEnum
from app.database import get_db
from app import schemas, crud
from app.dependencies import get_current_user, get_current_admin
from app.clients.programme_service import (
    ensure_programme_exists,
    ensure_cours_exists,
)


router = APIRouter(tags=["Admissions"], prefix="/admissions")


@router.get("/", response_model=List[schemas.AdmissionRead])
def list_admissions(
    db: Session = Depends(get_db),
    _: dict = Depends(get_current_admin),
    ):
    return crud.list_admissions(db)


@router.get("/user/{user_id}", response_model=list[schemas.AdmissionRead])
def list_admissions_for_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    is_admin = current_user.get("role") == "ADMIN"
    if not is_admin and current_user["sub"] != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Accès refusé.",
        )

    return crud.list_admissions_by_user(db, user_id)


@router.get("/{admission_id}", response_model=schemas.AdmissionRead)
def get_admission(
    admission_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    adm = crud.get_admission(db, admission_id)
    if not adm:
        raise HTTPException(status_code=404, detail="Admission not found")

    is_admin = current_user.get("role") == "ADMIN"
    if not is_admin and adm.user_id != int(current_user["sub"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Accès refusé.",
        )

    return adm


@router.post(
    "/",
    response_model=schemas.AdmissionRead,
    status_code=status.HTTP_201_CREATED,
)
def create_admission(
    admission: schemas.AdmissionCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
    ):
    user_id = current_user["sub"]
    # Double sécurité côté endpoint (optionnel)
    if admission.type_admission == TypeAdmissionEnum.PROGRAMME:
        ensure_programme_exists(admission.programme_id)
        # Sécurité supplémentaire : on force cours_id à None
        admission.cours_id = None
    elif admission.type_admission == TypeAdmissionEnum.COURS:
        ensure_cours_exists(admission.cours_id)
    return crud.create_admission(db, admission, user_id=user_id)


@router.patch(
    "/{admission_id}/status",
    response_model=schemas.AdmissionRead,
)
def update_admission_status(
    admission_id: int,
    payload: schemas.AdmissionStatusUpdate,
    db: Session = Depends(get_db),
    _: dict = Depends(get_current_admin),  # ADMIN only
):
    adm = crud.update_admission_status(db, admission_id, payload)
    if not adm:
        raise HTTPException(status_code=404, detail="Admission not found")
    return adm


@router.delete(
    "/{admission_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_admission(
    admission_id: int,
    db: Session = Depends(get_db),
    _: dict = Depends(get_current_admin),  # ADMIN only
):
    ok = crud.delete_admission(db, admission_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Admission not found")
    return None
