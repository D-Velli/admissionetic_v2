from typing import Optional
from pydantic import BaseModel, ConfigDict

# ---------- Programme ----------

class ProgrammeBase(BaseModel):
    codeProgramme: str
    nomProgramme: str


class ProgrammeCreate(ProgrammeBase):
    pass


class ProgrammeRead(ProgrammeBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


# ---------- Cours ----------

class CoursBase(BaseModel):
    codeCours: str
    titreCours: str
    programme_id: int


class CoursCreate(CoursBase):
    pass


class CoursRead(CoursBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
