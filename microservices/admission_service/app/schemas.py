# app/schemas.py
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, ConfigDict, model_validator
from decimal import Decimal

from app.models import TypeAdmissionEnum, StatutAdmissionEnum


class AdmissionBase(BaseModel):
    type_admission: TypeAdmissionEnum

    programme_id: Optional[int] = None
    cours_id: Optional[int] = None
    frais_admission: Optional[Decimal] = None
    commentaire: Optional[str] = None


class AdmissionCreate(AdmissionBase):
    """
    Règles :
    - type_admission = programme :
        - programme_id OBLIGATOIRE
        - cours_id INTERDIT (doit être null)
    - type_admission = cours :
        - cours_id OBLIGATOIRE
    """

    @model_validator(mode="after")
    def validate_type_vs_ids(self):
        if self.type_admission == TypeAdmissionEnum.PROGRAMME:
            if self.programme_id is None:
                raise ValueError(
                    "programme_id est obligatoire quand type_admission='programme'."
                )
            if self.cours_id is not None:
                raise ValueError(
                    "cours_id n'est pas autorisé quand type_admission='programme'."
                )

        elif self.type_admission == TypeAdmissionEnum.COURS:
            if self.cours_id is None:
                raise ValueError(
                    "cours_id est obligatoire quand type_admission='cours'."
                )

        return self


class AdmissionRead(AdmissionBase):
    id: int
    user_id: int
    status: StatutAdmissionEnum
    frais_admission: Optional[Decimal] = None
    date_demande: datetime
    date_maj: datetime

    model_config = ConfigDict(from_attributes=True)


class AdmissionStatusUpdate(BaseModel):
    status: StatutAdmissionEnum
    commentaire: Optional[str] = None
