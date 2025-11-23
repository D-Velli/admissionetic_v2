from __future__ import annotations #permet d’utiliser "CoursRead" dans ProgrammeRead sans problème de classes définies après.

from typing import List
from datetime import datetime, timedelta
from decimal import Decimal

from pydantic import BaseModel, ConfigDict
from app.models import StatusEnum


# ======================== PROGRAMME ========================

class ProgrammeBase(BaseModel):
    codeProgramme: str
    nomProgramme: str
    descProgramme: str | None = None
    publicCible: str | None = None
    dureeProgramme: timedelta | None = None   # Interval en DB
    prixProgramme: Decimal | None = None      # Numeric(5, 2)
    status: StatusEnum = StatusEnum.DISPONIBLE


class ProgrammeCreate(ProgrammeBase):
    # rien à ajouter, tout est déjà dans ProgrammeBase
    pass


class ProgrammeUpdate(BaseModel):
    codeProgramme: str | None = None
    nomProgramme: str | None = None
    descProgramme: str | None = None
    publicCible: str | None = None
    dureeProgramme: timedelta | None = None
    prixProgramme: Decimal | None = None
    status: StatusEnum | None = None


class ProgrammeInDBBase(ProgrammeBase):
    # id: int
    dateCreation: datetime | None = None

    # permet de lire directement des objets SQLAlchemy
    model_config = ConfigDict(from_attributes=True)


class ProgrammeRead(ProgrammeInDBBase):
    # on renvoie aussi la liste des cours du programme
    cours: List["CoursRead"] = []


# ========================== COURS ==========================

class CoursBase(BaseModel):
    codeCours: str
    titreCours: str
    prixCours: Decimal | None = None
    programme_id: int


class CoursCreate(CoursBase):
    pass


class CoursUpdate(BaseModel):
    codeCours: str | None = None
    titreCours: str | None = None
    prixCours: Decimal | None = None
    # programme_id: int | None = None


class CoursInDBBase(CoursBase):
    # id: int
    dateCreation: datetime | None = None

    model_config = ConfigDict(from_attributes=True)


class CoursRead(CoursInDBBase):
    pass
